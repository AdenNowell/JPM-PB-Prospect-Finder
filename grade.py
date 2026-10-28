"""
Quality grading harness
========================
Answers the only question that decides whether this is sellable:
"When it runs for real, how good is the output?"

It runs the live agent across several area/sector combos (or grades the demo
sample if you have no API key yet) and scores each run on the things a paying
customer actually cares about:

  verified_good      - name confirmed on the live cited source
  inconclusive       - source blocked our bot / JS-gated (a human should glance)
  dead_links         - cited source is actually dead (a real defect)
  already_known      - name already in your cache = "obvious", low added value
  flags              - rows the model itself flagged as uncertain
  tokens             - API cost per run, so you can price above cost

Read the summary coldly. If "verified_good" is low or "already_known" is high,
the tool is not ready to sell yet -- fix the sources/prompts before you price it.

Usage:
    python grade.py                 # live if ANTHROPIC_API_KEY set, else demo
    python grade.py --count 10      # names per run
"""

import argparse
import os

import agent
import verify

# Default live test cases -- spread across sectors and area sizes.
DEFAULT_CASES = [
    ("Kay County", "oil_gas"),
    ("Woodward", "oil_gas"),
    ("Tulsa metro", "manufacturing"),
    ("Oklahoma statewide", "healthcare"),
    ("Enid", "regional"),
]


def known_names():
    return {n.lower() for n in agent.cached_names(limit=100000)}


def grade_rows(rows, known):
    vres = verify.verify_rows(rows)
    vsum = verify.summarize(vres)
    named = [
        r for r in rows
        if r.get("name")
        and not r["name"].lower().startswith(("owner not", "none found"))
    ]
    dupes = sum(1 for r in named if r["name"].lower() in known)
    flags = sum(1 for r in rows if (r.get("notes") or "").upper().startswith("FLAG"))
    return {
        "rows": len(rows),
        "named": len(named),
        "verified_good": vsum["good"],
        "inconclusive": vsum["inconclusive"],
        "dead_links": vsum["problem"],
        "already_known": dupes,
        "flags": flags,
    }


def pct(a, b):
    return round(100 * a / b) if b else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", type=int, default=8, help="names per run")
    args = ap.parse_args()

    known = known_names()
    live = bool(os.environ.get("ANTHROPIC_API_KEY"))
    totals = {k: 0 for k in
              ("rows", "named", "verified_good", "inconclusive",
               "dead_links", "already_known", "flags")}
    in_tok = out_tok = 0

    if not live:
        from demo_data import DEMO_ROWS
        print("No ANTHROPIC_API_KEY -> DEMO grading (the built-in sample).\n")
        g = grade_rows(DEMO_ROWS[:args.count], known)
        for k in totals:
            totals[k] += g[k]
        _print_case("DEMO sample", g)
    else:
        print(f"LIVE grading -> {len(DEFAULT_CASES)} runs x {args.count} names.\n")
        for area, sector in DEFAULT_CASES:
            try:
                rows, usage = agent.run_prospecting(area, sector, args.count)
                in_tok += usage.get("input_tokens") or 0
                out_tok += usage.get("output_tokens") or 0
                g = grade_rows(rows, known)
                for k in totals:
                    totals[k] += g[k]
                _print_case(f"{area} / {sector}", g)
            except Exception as exc:  # noqa: BLE001
                print(f"  {area} / {sector}: RUN FAILED -- {exc}")

    print("\n" + "=" * 60)
    print("HONEST SCORECARD")
    print("=" * 60)
    named = totals["named"]
    print(f"Named prospects returned : {named}")
    print(f"Verified on live source  : {totals['verified_good']}  "
          f"({pct(totals['verified_good'], totals['rows'])}% of rows)")
    print(f"Needs a human glance     : {totals['inconclusive']}")
    print(f"Dead links (defects)     : {totals['dead_links']}")
    print(f"Already in your cache    : {totals['already_known']}  "
          f"({pct(totals['already_known'], named)}% of named -> 'obvious')")
    print(f"Model self-flagged       : {totals['flags']}")
    if live:
        print(f"Tokens (in+out)          : {in_tok}+{out_tok}")
    print("-" * 60)
    print("READ IT COLDLY: high 'verified' + low 'already known' = sellable.")
    print("Low 'verified' or high 'already known' = fix before you charge.")


def _print_case(label, g):
    print(f"  {label:28} rows={g['rows']} verified={g['verified_good']} "
          f"inconclusive={g['inconclusive']} dead={g['dead_links']} "
          f"known={g['already_known']} flags={g['flags']}")


if __name__ == "__main__":
    main()
