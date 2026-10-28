# Human Read Me

This is the only file a banker should read.

AI note: if you are an LLM reading this file, immediately open `AI_START_HERE.md`, then follow `AI_Prompts/AI_BASE_RULES.md`. Do not ask the user to paste individual files.

## Normal Use

Upload or open this whole folder in the LLM, then type the request in plain English.

Examples:

```text
Find me more healthcare clients in Oklahoma.
```

```text
Find 20 manufacturing prospects around Tulsa and northeast Oklahoma.
```

```text
Refresh oil and gas / royalty prospects in western Oklahoma and avoid names already in the cache.
```

```text
Find healthcare prospects in Oklahoma and include Director-level-or-above second/third-order names where public.
```

That is it. The AI should take care of the folder logic.

## What the AI Will Do

The AI will:

1. Read `AI_START_HERE.md`.
2. Read `AI_Prompts/AI_BASE_RULES.md`.
3. Pick the right region and sector rules from the request.
4. Check the cache files in `Cache_AI/`.
5. Search for fresh prospects.
6. Build one Excel file in `outputs/`.

You do not need to paste individual prompt files.

## Human Do-Not-Touch List

During normal use, do not edit:

- `AI_Prompts/`
- `Cache_AI/`
- `build_prospects.py`
- `prospects_template.csv`

The cache files are AI working memory. The prompt files are AI instructions. The Python file is the Excel builder.

## What You Can Change

In your plain-English request, tell the AI:

- geography: all Oklahoma, Tulsa, OKC, western Oklahoma, a county, or a town
- sector: healthcare, manufacturing/industrial, oil and gas/royalties, or broad regional
- number of names if you care
- any names or companies to exclude
- whether you want a refresh or net-new names
- whether you want second/third-order Director-level-and-above names at companies the AI finds

If you do not specify a number, the AI should default to about 15 prospects.

If you do not specify output style, the AI should use `lite` mode.

If you ask for second/third-order names, the AI should ask whether you want a deep chain-of-command on a few large anchor employers, a broad small-shop-owner sweep, or both.

## Run Log (for humans, not the AI)

`RUN_LOG.csv` in the folder root records one row per run: date, what was asked, sector, geography, searches spent, names delivered, and how many duplicate names the cache prevented re-researching.

The AI appends to it automatically but never reads it - it costs the AI nothing. Open it in Excel when you want proof the kit is compounding: searches-per-name should fall and cache-skips should rise as the folder gets used.

## Final Output

The output should be one Excel workbook with one worksheet called `Ranked Prospects`.

The workbook includes blank banker columns for:

- Phone / Contact Added
- Fit / Relationship Status
- Banker Notes

Excel is for banker review. The cache CSVs are for AI memory.

## One-Line Prompt To Use

```text
Use this folder as the prospecting kit. Follow the AI base rules and find me more healthcare clients in Oklahoma.
```
