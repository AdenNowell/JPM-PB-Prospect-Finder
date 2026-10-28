# Prospect Finder — one-button app

Turns the prompt kit into a web tool: a customer types an area + sector + count,
clicks **Find Prospects**, and downloads a private-bank-styled Excel of verified
Oklahoma prospects. The AI runs server-side through **your** Claude API key, so
the customer never brings their own AI or touches Python.

## Run it (Windows)

```powershell
cd "C:\Users\nowel\Downloads\Resuable Proespect Kit\app"
python -m pip install -r requirements.txt      # first time only
python server.py
```

Open http://127.0.0.1:5000

- **No API key set → DEMO mode.** Returns a built-in Oklahoma sample so you can
  see the whole click-to-Excel flow for free.
- **API key set → LIVE mode.** Runs a real web-search prospecting pass.

## Go live

1. Copy `.env.example` to `.env`.
2. Paste your key into `ANTHROPIC_API_KEY=` (from https://console.anthropic.com).
3. Restart `python server.py`. The header badge flips from DEMO to LIVE.

## How the money part works

- You hold ONE Claude API key (pay-as-you-go). Every customer run bills to it.
- `usage.db` (SQLite, created automatically) logs each run with token counts —
  that's your metering. No MongoDB or external database needed.
- Set `MONTHLY_RUN_LIMIT` to cap runs per customer per month (the subscription
  hook). Charge a flat monthly fee or per-run credits on top of your API cost.

## What it reuses (unchanged)

- `AI_Prompts/` — the research rules become the system prompt.
- `Cache_AI/CACHE_master_prospects.csv` — known names fed in so runs skip
  duplicates; live runs append new included names back to it.
- `build_prospects.py` — the Excel renderer, imported in-process (this also
  avoids the NUL-byte shell bug noted in AI_BASE_RULES).
- `outputs/` — where finished workbooks land.

## Files

| File | Purpose |
|------|---------|
| `server.py` | Flask web server, run endpoint, SQLite metering |
| `agent.py` | Claude API + web-search prospecting logic |
| `demo_data.py` | Built-in sample for DEMO mode |
| `templates/index.html` | The one-button UI |
| `.env` | Your API key + settings (you create this) |

## Compliance reminder

Every list carries the directional-signal / DNC-screening disclaimer. This tool
does not give investment advice and does not automate outreach (no calling or
texting — that's TCPA risk you don't want to own). It feeds your customer's
existing, compliance-approved workflow.
