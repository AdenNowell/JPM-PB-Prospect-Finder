"""
Prospecting agent
=================
Turns a plain-English request into verified Oklahoma wealth prospects by
running the existing prompt kit through the Claude API with the built-in
web-search tool. Returns rows as a list of dicts (the same schema
build_prospects.py already expects).

This module does the "AI" part. server.py does the web/button part and the
Excel rendering. Nothing here writes files or talks to the browser.
"""

import csv
import json
import os
import pathlib
import re

from anthropic import Anthropic

# ----------------------------------------------------------------------------
# Locate the existing kit (this file lives in <kit>/app/agent.py)
# ----------------------------------------------------------------------------
KIT_ROOT = pathlib.Path(__file__).resolve().parent.parent
PROMPTS = KIT_ROOT / "AI_Prompts"
CACHE = KIT_ROOT / "Cache_AI"

# Default model. Sonnet 5 is the cost/quality sweet spot for a paid-per-run
# tool. Bump to claude-opus-4-8 for hard runs by setting PROSPECT_MODEL.
DEFAULT_MODEL = os.environ.get("PROSPECT_MODEL", "claude-sonnet-5")

# Maps the UI dropdown value -> the kit's sector file. "regional" = no sector
# file (broad Oklahoma sweep), per AI_BASE_RULES.
SECTOR_FILES = {
    "oil_gas": "AI_SECTOR_OIL_GAS_ROYALTIES.md",
    "manufacturing": "AI_SECTOR_MANUFACTURING.md",
    "healthcare": "AI_SECTOR_HEALTHCARE.md",
    "regional": None,
}

SECTOR_LABELS = {
    "oil_gas": "oil & gas / royalties / minerals",
    "manufacturing": "manufacturing / industrial",
    "healthcare": "healthcare",
    "regional": "broad regional (highest-yield sectors)",
}

# The exact column order build_prospects.py reads.
SCHEMA = [
    "rank", "name", "city_county", "sector", "role_type", "business",
    "wealth_signal", "source_label", "source_url", "confidence", "why_fit",
    "hook", "notes", "more_available_count", "more_available_note",
]

# This overrides the "write prospects.csv and run build_prospects.py"
# instructions in the kit rules, because the app does that part itself.
OUTPUT_CONTRACT = """
## APP OUTPUT CONTRACT (this overrides any file-writing / build steps above)

You are running inside an automated web app. Do NOT write files, do NOT run or
mention build_prospects.py, do NOT ask the user any clarifying questions, and
do NOT append to cache files yourself. The app handles all of that.

Do your normal research using the web_search tool. Follow every rule above for
who to find, wealth signals, confidence, ranking, and compliance.

When finished, output your answer as ONE fenced ```json code block and nothing
else -- no preamble, no explanation after it. The block must be a JSON array.
Each element is an object with EXACTLY these string keys:

rank, name, city_county, sector, role_type, business, wealth_signal,
source_label, source_url, confidence, why_fit, hook, notes,
more_available_count, more_available_note

Rules for the JSON:
- Every included person must have a real public source_url you actually opened
  via web_search. If you cannot verify a real person, do not invent one.
- If a target company exists but you could not name the owner, you may include a
  row with name "Owner not publicly identified" and start notes with "FLAG:".
- Leave more_available_count / more_available_note as "" unless relevant.
- Keep every cell concise. No line breaks inside a value.
- Return ONLY the json block.
"""


def _read(path):
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def build_system_prompt(sector):
    """Assemble the kit's rules for this sector into one system prompt."""
    parts = [
        _read(PROMPTS / "AI_BASE_RULES.md"),
        _read(PROMPTS / "AI_REGION_OKLAHOMA.md"),
    ]
    sector_file = SECTOR_FILES.get(sector)
    if sector_file:
        parts.append(_read(PROMPTS / sector_file))
    parts.append(OUTPUT_CONTRACT)
    return "\n\n---\n\n".join(p for p in parts if p.strip())


def cached_names(limit=300):
    """Names already in the master cache, so the model skips duplicates."""
    master = CACHE / "CACHE_master_prospects.csv"
    if not master.exists():
        return []
    names = []
    try:
        with open(master, newline="", encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                name = (row.get("name") or "").strip()
                if name:
                    names.append(name)
    except OSError:
        return []
    return names[:limit]


def _extract_json_array(text):
    """Pull the JSON array out of the model's final message."""
    if not text:
        return []
    # Prefer a fenced ```json block.
    fence = re.search(r"```(?:json)?\s*(\[.*?\])\s*```", text, re.DOTALL)
    raw = fence.group(1) if fence else None
    if raw is None:
        # Fall back to the first bare [ ... ] that parses.
        start = text.find("[")
        end = text.rfind("]")
        raw = text[start:end + 1] if start != -1 and end > start else None
    if raw is None:
        return []
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []


def normalize_rows(rows):
    """Force every row to the exact schema keys as strings."""
    clean = []
    for i, row in enumerate(rows, 1):
        if not isinstance(row, dict):
            continue
        out = {k: str(row.get(k, "") or "").strip() for k in SCHEMA}
        if not out.get("rank"):
            out["rank"] = str(i)
        clean.append(out)
    return clean


def run_prospecting(area, sector, count, exclude="", api_key=None, model=None):
    """
    Run one real prospecting pass. Returns (rows, usage_dict).
    Raises if the API key is missing/invalid or the call fails.
    """
    key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        raise RuntimeError("No ANTHROPIC_API_KEY set. Add one to app/.env to go live.")

    client = Anthropic(api_key=key)
    system = build_system_prompt(sector)
    skip = cached_names()
    skip_line = (
        "Already-known names to SKIP (do not return these): "
        + "; ".join(skip)
        if skip else "No prior names cached yet."
    )
    sector_label = SECTOR_LABELS.get(sector, sector)

    user = (
        f"Find {count} net-new {sector_label} wealth-prospects in {area}, Oklahoma. "
        f"Use lite depth (owner/anchor name per company) unless a company clearly "
        f"warrants more. {skip_line}. "
        + (f"Also exclude: {exclude}. " if exclude.strip() else "")
        + "Return the json array per the output contract."
    )

    resp = client.messages.create(
        model=model or DEFAULT_MODEL,
        max_tokens=8000,
        system=system,
        tools=[{
            "type": "web_search_20250305",
            "name": "web_search",
            "max_uses": max(8, int(count) + 3),
        }],
        messages=[{"role": "user", "content": user}],
    )

    text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
    rows = normalize_rows(_extract_json_array(text))

    usage = {
        "input_tokens": getattr(resp.usage, "input_tokens", None),
        "output_tokens": getattr(resp.usage, "output_tokens", None),
        "model": model or DEFAULT_MODEL,
    }
    return rows, usage
