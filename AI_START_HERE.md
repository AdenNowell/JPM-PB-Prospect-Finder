# AI Start Here

If the user asks for prospecting, start here. Do not ask the user to paste individual files.

## Fast Route

1. Read `AI_Prompts/AI_BASE_RULES.md`.
2. Read `AI_Prompts/AI_BANKER_PROFILE.md` - who this run is for and what counts as a fit. Read it on EVERY run.
3. For Oklahoma work, read `AI_Prompts/AI_REGION_OKLAHOMA.md`.
4. Pick only the sector file required by the request:
   - healthcare: `AI_Prompts/AI_SECTOR_HEALTHCARE.md`
   - manufacturing / industrial: `AI_Prompts/AI_SECTOR_MANUFACTURING.md`
   - oil, gas, royalties, minerals, land, ranch: `AI_Prompts/AI_SECTOR_OIL_GAS_ROYALTIES.md`
   - ONE named private company (its execs/engineers/board): `AI_Prompts/AI_MODE_SINGLE_COMPANY.md` (mode file - overrides some base rules; skip sector/region files unless relevant)
5. Read the five cache files in `Cache_AI/`:
   - `CACHE_master_prospects.csv` (skip cached names)
   - `CACHE_rejected_duplicates.csv` (skip rejected names)
   - `CACHE_sources_checked.csv`
   - `CACHE_high_yield_sources.csv` (start discovery here)
   - `CACHE_do_not_contact.csv` (never include these names in a list)
6. Write `prospects.csv`. Leave `phone_contact` and `email` BLANK - contacts are enriched after the build, never during research.
7. Run `build_prospects.py` (if the shell's copy looks truncated or errors on NUL bytes, see the environment-bug notes in `AI_BASE_RULES.md` Build Output — run a clean temp copy, never rewrite the original).
8. Save the Excel workbook in `outputs/` with a date-stamped filename (`Prospect_List_[AREA]_[YYYY-MM-DD].xlsx`).
9. Contact Enrichment Pass (AFTER the workbook exists): run ONE batched ZoomInfo `enrich_contacts` call covering every name at once - never one call per person. Skip anyone already marked `resolved` or `no-match` in `CACHE_master_prospects.csv`. Write results into the workbook. Full rules in `AI_BASE_RULES.md` Contact Enrichment Pass.
10. APPEND this run's results to all cache files (never delete existing rows), including `contact_status` on every master-prospect row. Do not skip this step - it is what makes the next run cheaper.

## No-Code Fallback

If you cannot run Python or write files (chat-only web-search LLM):

1. Skip `build_prospects.py`.
2. Output `prospects.csv` as one fenced CSV block in chat, using the exact header in `AI_BASE_RULES.md`.
3. Output cache-update rows as fenced CSV blocks labeled `CACHE DELTAS` (one per cache file touched).
4. Tell the human to paste both back into the folder. (If you CAN write files, do not use this fallback - append the caches directly per `AI_BASE_RULES.md`.)

## Defaults And Depth

All defaults (geography, sector, count, mode, depth) and the second/third-order depth protocol live in `AI_Prompts/AI_BASE_RULES.md`. Follow that file; do not guess.

## Do Not Read Unless Asked

- `HUMAN_READ_ME.md`
- `RUN_LOG.csv` (append one summary row at end of run WITHOUT reading it - use a shell append; it is human reporting, not AI memory)
- `outputs/`
- `__pycache__/`
- `.git/`
- `.agents/`
- old Excel workbooks

The expensive work is search and verification. Keep folder-reading tight.

Internet access is required for fresh prospecting. If you cannot search the web, do not invent names; say internet access is needed.
