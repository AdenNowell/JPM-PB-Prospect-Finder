# AI Mode - Single Private Company Deep Dive

Use this file when the user names ONE specific private company and wants the people in it as private-bank prospects (founders, C-suite, engineers, leadership, board). This mode OVERRIDES parts of `AI_BASE_RULES.md`; everything not overridden still applies (compliance, CSV schema, cache protocol, build step).

## Overrides Of Base Rules

- The famous-name auto-reject is suspended for THIS company's people. The user chose the company; a CEO with press coverage is still deliverable. Wikipedia-level celebrities (national fame) still get flagged in `notes`, not dropped.
- The 3-names-per-company cap is suspended. Default 15 names, or the user's count.
- Geography default is wherever the company is, not Oklahoma.
- Below-Director titles MAY be included when the person is a likely early-employee equity holder (see Equity Sweep Logic). Start `notes` with `FLAG:` and say why.

## Preconceived Logic: How Private-Company Wealth Works

Assume this model before searching; it tells you who matters and why.

1. Equity concentrates at founding. Founders and the first ~10 employees hold the large sweeps. Title today matters less than join date. A "Manager" who was employee #1 often out-owns a VP hired at Series C.
2. Each funding round dilutes but re-prices. A founder at a company that raised $60M+ at a step-up is paper-rich even after dilution. Total raised + round recency is your proxy for stake value.
3. Wealth is ILLIQUID until an event. These people are FUTURE-HNW, not current HNW. The bank's play is to arrive before the liquidity event: acquisition, IPO, secondary sale, tender offer.
4. C-suite hired post-Series B get option packages (~0.5-2%); VPs less; late employees very little. Rank accordingly.
5. Board of DIRECTORS seats at VC-backed privates are mostly investor partners (fund wealth, usually out-of-footprint) plus founders. Board of ADVISORS members are often local operators/owners with their own companies - frequently better prospects than the directors.
6. External board/advisor members bring their OWN wealth base (their company, their prior exits). Assess them on that, not on the target company.

## Equity Sweep Ladder (who to include, in order)

1. Founders / co-founders (any current title, even "retired" or advisory)
2. Founding-family members in the business
3. Board of Directors - independent and operator seats (skip pure VC-fund partners unless local/notable)
4. Board of Advisors - especially owner-operators of their own firms
5. C-suite (CEO, CFO, CTO, COO, GC/Secretary, Chief of Staff, Chief Engineer/Scientist)
6. VP / Senior Director level
7. Named early employees (first engineer, first sales hire, "employee #1" stories) - include below-Director with a FLAG
8. Recently DEPARTED execs/founders - they often just sold shares in a secondary; check where they went

## Future-HNW Signals (what makes a name rank higher)

- co-founder or founding-family status
- named on company patents (IP + equity double signal)
- present through 2+ funding rounds (vesting depth)
- promoted internally (refreshed grants)
- prior exit or prior founder role elsewhere
- late-career exec at a young company (took equity over salary)
- company signals: big raise in last 18 months, step-up valuation, defense/gov contracts, new facility construction, pre-IPO secondary market listings (Forge/EquityZen), acquisition rumors
- personal liquidity signals: new LLC formations, real-estate purchases, donations, angel investments

## Where To Look (search order, cheapest first)

1. Company website team/about/leadership page - one fetch often yields 8-12 names with titles
2. Company newsroom/press releases - funding, appointments, board/advisor announcements
3. Funding press (PRNewswire, TechCrunch, trade press) - names investors, board seats, quotes with titles
4. Org-chart aggregators: theorg.com, Crunchbase people page, PitchBook/CB Insights profile pages (free tier text)
5. LinkedIn company page + employee-spotlight posts - early-employee stories, promotions
6. State SoS filings - registered officers/directors of the entity
7. Patent search (Google Patents, assignee = company) - inventor names = technical equity holders
8. Pre-IPO marketplaces (Forge, EquityZen, Hiive) - confirms secondary liquidity exists
9. Local business journals (e.g., Dallas Business Journal) - profiles, "40 under 40", facility stories

Budget: fetching the team page and 2-3 press releases replaces 10+ people-searches. Do those FIRST, then use searches only to fill gaps (board members, early employees, departed founders).

## Ranking Within One Company

1. Founders and owner-operator board/advisors
2. C-suite with tenure through multiple rounds
3. VP/Director with tenure
4. Board advisors assessed on their own company wealth
5. Early employees (FLAGged)
Downgrade: hired within last 12 months, no equity signal, pure VC-fund partners, out-of-footprint people (note but keep if user asked for the full roster).

## Output

Same schema, builder, cache appends, and RUN_LOG row as `AI_BASE_RULES.md`. Full mode is the default for this mode (notes/compliance column matter here). Suggested title/filename:

```text
--title "Wealth-Prospecting Candidate List - [COMPANY], [CITY] [ST]" --out "outputs/Prospect_List_[COMPANY]_[YYYY-MM-DD].xlsx"
```

If the formal Board of Directors is not publicly disclosed (common), say so in the CEO row's `notes` and name the lead investors likely holding seats. Do not invent director names.
