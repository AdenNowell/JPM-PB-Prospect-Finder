#!/usr/bin/env python3
"""
REUSABLE PROSPECT-LIST BUILDER - write this ONCE, reuse forever.
=================================================================
Do NOT rewrite this file for each new town. It is the renderer.
Each run should produce only the data CSV, then call this script.

USAGE
-----
python build_prospects.py \
    --title "Wealth-Prospecting Candidate List - <TOWNS>, OK (<COUNTY> County)" \
    --mode lite \
    --data prospects.csv \
    --out "outputs/Prospect_List_<TOWNS>.xlsx"

CSV SCHEMA
----------
rank,name,city_county,sector,role_type,business,signal_and_fit,source_label,source_url,confidence,notes,more_available_count,more_available_note

Optional banker columns are accepted if present:
phone_contact,email,relationship_status,banker_notes

`confidence` is read for ranking/cache purposes but is NOT rendered as a
column. `hook` is no longer rendered either; it is ignored if still present.

Backward compatibility: older CSVs that still have separate wealth_signal and
why_fit columns (and no signal_and_fit) are joined into one "Signal & Fit"
column automatically, so previous prospects.csv files still build.

Rendering notes (v3):
  - Private-bank beige/bronze palette, gridlines off, landscape print fit-to-width.
  - No intro banner rows: the header row is row 1 and data starts at row 2.
  - --title sets the worksheet tab name (cleaned and capped at Excel's 31
    chars); --banner is accepted for CLI compatibility and ignored.
  - Data-row heights are estimated from wrapped text so nothing is clipped.
  - "Contact List Check" is an empty, uncolored column the banker fills in
    after screening against internal existing-client / suppression / DNC lists.
  - Full mode: AI research notes render as a cell comment on the Name cell
    (FLAG rows tint the Name cell).
  - source_label is clickable text; source_url is the hyperlink target.
  - No conditional coloring anywhere: the only tints are alternating row
    shading and the FLAG tint on a Name cell.
"""

import argparse
import csv
import math
import os
import sys

from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.properties import PageSetupProperties


# J.P. Morgan Private Bank-inspired palette: espresso, bronze, cream, beige.
BRONZE = "7A6448"     # column headers
BEIGE_ALT = "F7F4EC"  # alternating rows
WHITE = "FFFFFF"
FLAG = "E9CFC0"       # FLAG tint on a Name cell
LINK = "155CB0"       # readable link blue
# Retained palette reference, no longer applied (no banner rows, no conditional
# coloring): ESPRESSO 3B2B1D, CREAM F5F1E6, INKBROWN 5A4632, SAGE D9E5CE,
# TAN F1E3C2, WARMGREY E7E3D9.

thin = Side(style="thin", color="D9D0BF")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)

DEFAULT_BANNER = (
    "Open-source / public-records research only. Wealth figures are DIRECTIONAL signals, not verified "
    "financials - screen every name against internal do-not-contact / existing-client / DNC lists before any outreach. "
    "Independent O&G operators and mineral/royalty owners are usually LLC/records-veiled and, if not nameable here, "
    "require a county clerk/assessor + minerals-data (Enverus) pull."
)


INVALID_SHEET_CHARS = set("[]:*?/\\")


def sheet_title(title):
    """Turn --title into a clean worksheet tab name (Excel caps tabs at 31 chars)."""
    text = " ".join((title or "").split())
    parts = [p.strip() for p in text.split(" - ") if p.strip()]
    # Prefer the last chunk that actually names a place or subject, so
    # "Wealth-Prospecting Candidate List - Woodward, OK" becomes "Woodward, OK"
    # and a trailing date fragment never becomes the tab name.
    for part in reversed(parts):
        if any(ch.isalpha() for ch in part):
            text = part
            break
    text = "".join(ch for ch in text if ch not in INVALID_SHEET_CHARS).strip()
    if len(text) > 31:
        text = text[:31].rstrip(" ,-")
    return text or "Ranked Prospects"


def more_available_comment(data):
    count = (data.get("more_available_count") or "").strip()
    note = (data.get("more_available_note") or "").strip()
    if not count and not note:
        return None

    count_text = count if count else "Additional"
    if count:
        try:
            count_text = str(int(float(count)))
        except ValueError:
            count_text = count

    text = (
        f"{count_text} additional named Director-level-or-above people appear publicly for this company. "
        "The full chain of command was not pulled in this pass."
    )
    if note:
        text += f" {note}"
    return text


def signal_and_fit(data):
    """Merged 'Signal & Fit' text, with fallback to the old two-column schema."""
    merged = (data.get("signal_and_fit") or "").strip()
    if merged:
        return merged
    parts = [
        (data.get("wealth_signal") or "").strip(),
        (data.get("why_fit") or "").strip(),
    ]
    return " — ".join(part for part in parts if part)


def estimate_lines(text, width):
    """Rough wrapped-line count for a cell of the given character width."""
    if not text:
        return 1
    lines = 0
    for chunk in str(text).split("\n"):
        lines += max(1, math.ceil(len(chunk) / max(1.0, width * 0.95)))
    return lines


def build(title, mode, data_path, out_path, banner=DEFAULT_BANNER):
    with open(data_path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise ValueError("No data rows found in " + data_path)

    lite = mode == "lite"
    headers = [
        "Rank",
        "Name",
        "City (County)",
        "Sector",
        "Role Type",
        "Profession / Business",
        "Signal & Fit",
        "Source (link)",
        "Contact List Check",
        "Phone / Contact Added",
        "Email",
        "Fit / Relationship Status",
        "Banker Notes",
    ]
    ncol = len(headers)

    widths = [6, 24, 18, 15, 12, 28, 55, 16, 16, 13, 24, 13, 20]

    wb = Workbook()
    ws = wb.active
    ws.title = sheet_title(title)
    last = get_column_letter(ncol)

    ws.sheet_view.showGridLines = False
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr = PageSetupProperties(fitToPage=True)

    # No intro banner rows - the sheet opens straight into the header row.
    # title/banner are accepted for CLI compatibility and intentionally unused.
    header_row = 1
    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=header_row, column=col, value=header)
        cell.font = Font(name="Arial", bold=True, size=10, color=WHITE)
        cell.fill = PatternFill("solid", fgColor=BRONZE)
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = BORDER
    ws.row_dimensions[header_row].height = 30

    row_num = header_row + 1
    for data in rows:
        base_fill = BEIGE_ALT if row_num % 2 == 0 else WHITE
        values = [
            data.get("rank", ""),
            data.get("name", ""),
            data.get("city_county", ""),
            data.get("sector", ""),
            data.get("role_type", ""),
            data.get("business", ""),
            signal_and_fit(data),
            data.get("source_label", ""),
            "",  # Contact List Check - banker fills this in after screening
            data.get("phone_contact", ""),
            data.get("email", ""),
            data.get("relationship_status", ""),
            data.get("banker_notes", ""),
        ]

        for col, value in enumerate(values, 1):
            cell = ws.cell(row=row_num, column=col, value=value)
            cell.border = BORDER
            cell.alignment = Alignment(
                horizontal="center" if col in (1, 5, 9) else "left",
                vertical="center" if col <= 5 else "top",
                wrap_text=True,
            )
            cell.font = Font(name="Arial", size=9)
            cell.fill = PatternFill("solid", fgColor=base_fill)

        name_cell = ws.cell(row=row_num, column=2)
        name_cell.font = Font(name="Arial", size=9, bold=True)

        notes = (data.get("notes", "") or "").strip()
        if not lite and notes:
            comment = Comment(f"AI research notes: {notes}", "Prospecting Kit")
            comment.width = 320
            comment.height = 130
            name_cell.comment = comment
            if notes.upper().startswith("FLAG"):
                name_cell.fill = PatternFill("solid", fgColor=FLAG)

        business_cell = ws.cell(row=row_num, column=6)
        comment_text = more_available_comment(data)
        if comment_text:
            comment = Comment(comment_text, "Prospecting Kit")
            comment.width = 320
            comment.height = 130
            business_cell.comment = comment

        source_cell = ws.cell(row=row_num, column=8)
        if data.get("source_url"):
            source_cell.hyperlink = data["source_url"]
            source_cell.font = Font(name="Arial", size=9, color=LINK, underline="single")

        max_lines = max(
            estimate_lines(value, widths[col - 1]) for col, value in enumerate(values, 1)
        )
        ws.row_dimensions[row_num].height = min(110, max(18, max_lines * 12 + 6))

        row_num += 1

    for idx, width in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(idx)].width = width
    ws.freeze_panes = f"A{header_row + 1}"
    ws.auto_filter.ref = f"A{header_row}:{last}{row_num - 1}"
    out_dir = os.path.dirname(out_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    wb.save(out_path)
    print(f"Saved {out_path} | mode={mode} | rows={len(rows)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", required=True)
    parser.add_argument("--mode", choices=["lite", "full"], default="lite")
    parser.add_argument("--data", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--banner", default=DEFAULT_BANNER)
    args = parser.parse_args()
    try:
        build(args.title, args.mode, args.data, args.out, args.banner)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: build failed - {exc}", file=sys.stderr)
        sys.exit(1)
