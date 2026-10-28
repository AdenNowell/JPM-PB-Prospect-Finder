"""
Source verification
====================
A safety net that catches the things that would embarrass a customer: a dead
source link, or a name that doesn't appear on the page it cites (a sign the
model may have invented the source).

For each prospect row it fetches source_url and sorts it into one of three
honest buckets:

  GOOD        - page loads and the person's name is on it (or it's an
                intentional "owner not named" FLAG row).
  INCONCLUSIVE- the site blocked our automated fetch (403/401/429/SSL) or is
                JavaScript-gated so the name isn't in the raw HTML. This is
                NOT evidence the person is fake -- lots of real sources
                (LinkedIn, D&B, ZoomInfo, county sites) block bots. It just
                means a human should glance before outreach.
  PROBLEM     - the link is actually dead (404/5xx) or missing. A real red flag.

The point is to auto-catch the obvious junk, while being honest that a blocked
fetch is not a verdict on the person.
"""

import concurrent.futures as cf

import requests

# Browser-like headers cut down on false 403s from sites that block bare bots.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/125.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

GOOD = {"verified", "flagged_unnamed"}
INCONCLUSIVE = {"blocked", "js_or_name_missing"}
PROBLEM = {"broken", "no_source"}

BUCKET = {
    "verified": "good", "flagged_unnamed": "good",
    "blocked": "inconclusive", "js_or_name_missing": "inconclusive",
    "broken": "problem", "no_source": "problem",
}


def _last_name(name):
    parts = [p.strip(".,'\"") for p in name.split() if len(p.strip(".,'\"")) > 2]
    return parts[-1].lower() if parts else ""


def verify_row(row, timeout=12):
    name = (row.get("name") or "").strip()
    url = (row.get("source_url") or "").strip()
    out = {"verdict": "unverified", "bucket": "problem", "detail": ""}

    unnamed = (not name) or name.lower().startswith("owner not") or name.lower() == "none found"
    if not url:
        out.update(verdict="no_source", bucket="problem", detail="no source url")
        return out
    try:
        r = requests.get(url, timeout=timeout, headers=HEADERS, allow_redirects=True)
        code = r.status_code
        if code in (401, 403, 429):
            out.update(verdict="blocked", detail=f"site blocked automated fetch (HTTP {code})")
        elif code == 404 or code >= 500:
            out.update(verdict="broken", detail=f"dead link (HTTP {code})")
        elif code == 200 and unnamed:
            out.update(verdict="flagged_unnamed", detail="owner intentionally not named")
        elif code == 200:
            last = _last_name(name)
            if last and last in r.text.lower():
                out.update(verdict="verified", detail="name found on cited source")
            else:
                out.update(verdict="js_or_name_missing",
                           detail="name not in raw HTML (may be JS-gated)")
        else:
            out.update(verdict="blocked", detail=f"unexpected HTTP {code}")
    except requests.exceptions.SSLError:
        out.update(verdict="blocked", detail="SSL error (site may block bots)")
    except requests.RequestException as exc:
        out.update(verdict="broken", detail=type(exc).__name__)

    out["bucket"] = BUCKET.get(out["verdict"], "problem")
    return out


def verify_rows(rows, max_workers=6):
    results = [None] * len(rows)
    if not rows:
        return results
    with cf.ThreadPoolExecutor(max_workers=max_workers) as ex:
        futs = {ex.submit(verify_row, r): i for i, r in enumerate(rows)}
        for fut in cf.as_completed(futs):
            results[futs[fut]] = fut.result()
    return results


def summarize(results):
    results = [r for r in results if r]
    n = len(results)
    good = sum(1 for r in results if r["bucket"] == "good")
    inconclusive = sum(1 for r in results if r["bucket"] == "inconclusive")
    problem = sum(1 for r in results if r["bucket"] == "problem")
    return {
        "total": n,
        "good": good,
        "inconclusive": inconclusive,
        "problem": problem,
        "good_pct": round(100 * good / n) if n else 0,
    }


if __name__ == "__main__":
    from demo_data import DEMO_ROWS
    res = verify_rows(DEMO_ROWS)
    for row, vr in zip(DEMO_ROWS, res):
        print(f"{vr['bucket']:12} {vr['verdict']:20} | {row['name'][:24]:24} | {vr['detail']}")
    print("summary:", summarize(res))
