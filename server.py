"""
One-button prospecting app
==========================
Serves a single page: pick an area + sector + count, click "Find Prospects",
get a private-bank-styled Excel of verified Oklahoma prospects.

- The "AI" is agent.py (Claude API + web search), run server-side with YOUR key.
- The Excel is rendered by the existing build_prospects.py (imported in-process,
  which also avoids the NUL-byte shell bug documented in AI_BASE_RULES).
- Usage is metered in a local SQLite file (app/usage.db) -- the hook for
  charging a subscription or credits later. No MongoDB needed.

Run:
    cd "<this folder>/app"
    python server.py
Then open http://127.0.0.1:5000
"""

import csv
import datetime as dt
import os
import pathlib
import re
import sqlite3
import sys
import traceback

from flask import Flask, jsonify, render_template, request, send_from_directory

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

APP_DIR = pathlib.Path(__file__).resolve().parent
KIT_ROOT = APP_DIR.parent
OUTPUTS = KIT_ROOT / "outputs"
RUNS = APP_DIR / "_runs"
DB_PATH = APP_DIR / "usage.db"

# Import the existing Excel renderer from the kit root.
sys.path.insert(0, str(KIT_ROOT))
import build_prospects  # noqa: E402
import agent  # noqa: E402
import verify  # noqa: E402
from demo_data import DEMO_ROWS  # noqa: E402

app = Flask(__name__)

SECTOR_LABEL_FOR_TITLE = {
    "oil_gas": "Oil & Gas / Royalties",
    "manufacturing": "Manufacturing / Industrial",
    "healthcare": "Healthcare",
    "regional": "Regional",
}

# Optional soft cap per customer per calendar month (the subscription hook).
# 0 or unset = unlimited.
MONTHLY_RUN_LIMIT = int(os.environ.get("MONTHLY_RUN_LIMIT", "0"))


# ----------------------------------------------------------------------------
# Usage metering (SQLite)
# ----------------------------------------------------------------------------
def db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT, customer TEXT, area TEXT, sector TEXT, count INTEGER,
            mode TEXT, status TEXT, input_tokens INTEGER, output_tokens INTEGER,
            model TEXT, out_file TEXT
        )"""
    )
    return conn


def runs_this_month(conn, customer):
    ym = dt.date.today().strftime("%Y-%m")
    cur = conn.execute(
        "SELECT COUNT(*) FROM runs WHERE customer=? AND status='ok' "
        "AND substr(ts,1,7)=?",
        (customer, ym),
    )
    return cur.fetchone()[0]


def log_run(conn, **kw):
    conn.execute(
        "INSERT INTO runs (ts, customer, area, sector, count, mode, status, "
        "input_tokens, output_tokens, model, out_file) "
        "VALUES (:ts,:customer,:area,:sector,:count,:mode,:status,"
        ":input_tokens,:output_tokens,:model,:out_file)",
        kw,
    )
    conn.commit()


# ----------------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------------
def safe_slug(text):
    slug = re.sub(r"[^A-Za-z0-9]+", "_", text).strip("_")
    return slug[:40] or "Oklahoma"


def write_csv(rows, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=agent.SCHEMA)
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, "") for k in agent.SCHEMA})


def append_master_cache(rows):
    """Append included rows to the master cache (append-only, never rewrites)."""
    master = KIT_ROOT / "Cache_AI" / "CACHE_master_prospects.csv"
    if not master.exists():
        return
    today = dt.date.today().isoformat()
    with open(master, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        for r in rows:
            name = (r.get("name") or "").strip()
            if not name or name.lower().startswith("owner not"):
                continue
            w.writerow([
                name, r.get("business", ""), r.get("sector", ""),
                r.get("role_type", ""), r.get("city_county", ""), today,
                "included", r.get("confidence", ""), r.get("why_fit", ""),
                r.get("source_url", ""),
            ])


# ----------------------------------------------------------------------------
# Routes
# ----------------------------------------------------------------------------
@app.route("/")
def index():
    has_key = bool(os.environ.get("ANTHROPIC_API_KEY"))
    return render_template("index.html", live=has_key)


@app.route("/run", methods=["POST"])
def run():
    data = request.get_json(force=True, silent=True) or {}
    area = (data.get("area") or "Oklahoma statewide").strip()
    sector = data.get("sector") or "regional"
    exclude = (data.get("exclude") or "").strip()
    customer = (data.get("customer") or "demo").strip() or "demo"
    try:
        count = max(1, min(40, int(data.get("count") or 15)))
    except (TypeError, ValueError):
        count = 15

    conn = db()

    if MONTHLY_RUN_LIMIT and runs_this_month(conn, customer) >= MONTHLY_RUN_LIMIT:
        conn.close()
        return jsonify({
            "error": f"Monthly run limit ({MONTHLY_RUN_LIMIT}) reached for this plan."
        }), 402

    live = bool(os.environ.get("ANTHROPIC_API_KEY"))
    usage = {"input_tokens": None, "output_tokens": None, "model": None}

    try:
        if live:
            rows, usage = agent.run_prospecting(area, sector, count, exclude=exclude)
            mode_used = "live"
        else:
            rows = DEMO_ROWS[:count]
            mode_used = "demo"

        if not rows:
            raise RuntimeError(
                "No verifiable prospects came back. Try a broader area or a "
                "different sector."
            )

        # Verify each cited source: dead-link + hallucination safety net.
        vresults = verify.verify_rows(rows)
        vsummary = verify.summarize(vresults)
        for row, vr in zip(rows, vresults):
            row["_bucket"] = vr["bucket"]
            if vr["bucket"] == "problem":
                if not row.get("confidence", "").lower().startswith("low"):
                    row["confidence"] = "Low"
                note = (row.get("notes") or "").strip()
                if not note.upper().startswith("FLAG"):
                    row["notes"] = f"FLAG: source not verified ({vr['detail']}). {note}".strip()

        RUNS.mkdir(exist_ok=True)
        OUTPUTS.mkdir(exist_ok=True)
        today = dt.date.today().isoformat()
        slug = safe_slug(area)
        csv_path = RUNS / f"prospects_{slug}_{today}.csv"
        out_name = f"Prospect_List_{slug}_{today}.xlsx"
        out_path = OUTPUTS / out_name

        write_csv(rows, csv_path)
        title = (
            f"Wealth-Prospecting Candidate List - {area}, OK "
            f"({SECTOR_LABEL_FOR_TITLE.get(sector, 'Regional')})"
        )
        build_prospects.build(title, "lite", str(csv_path), str(out_path))

        if live:
            append_master_cache(rows)

        log_run(
            conn, ts=dt.datetime.now().isoformat(timespec="seconds"),
            customer=customer, area=area, sector=sector, count=len(rows),
            mode=mode_used, status="ok",
            input_tokens=usage.get("input_tokens"),
            output_tokens=usage.get("output_tokens"),
            model=usage.get("model"), out_file=out_name,
        )
        conn.close()

        preview = []
        for r in rows:
            item = {k: r.get(k, "") for k in
                    ("rank", "name", "city_county", "business", "confidence", "source_url")}
            item["checked"] = r.get("_bucket", "")
            preview.append(item)
        return jsonify({
            "ok": True, "mode": mode_used, "count": len(rows),
            "download": f"/download/{out_name}", "filename": out_name,
            "preview": preview, "usage": usage, "verification": vsummary,
        })

    except Exception as exc:  # noqa: BLE001
        traceback.print_exc()
        try:
            log_run(
                conn, ts=dt.datetime.now().isoformat(timespec="seconds"),
                customer=customer, area=area, sector=sector, count=count,
                mode="live" if live else "demo", status="error",
                input_tokens=usage.get("input_tokens"),
                output_tokens=usage.get("output_tokens"),
                model=usage.get("model"), out_file="",
            )
            conn.close()
        except Exception:  # noqa: BLE001
            pass
        return jsonify({"error": str(exc)}), 500


@app.route("/download/<path:name>")
def download(name):
    return send_from_directory(OUTPUTS, name, as_attachment=True)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    print(f"Prospecting app on http://127.0.0.1:{port}  "
          f"({'LIVE (API key found)' if os.environ.get('ANTHROPIC_API_KEY') else 'DEMO mode - no API key'})")
    app.run(host="127.0.0.1", port=port, debug=False)
