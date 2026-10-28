# AI Region Rules - Oklahoma

Use this file for Oklahoma-wide or Oklahoma regional prospecting.

## Oklahoma source priority

Tags: `AI-SEARCHABLE` = search it directly. `HUMAN-PULL` = form/portal a web-search LLM usually cannot drive; never burn searches on it — write a `FLAG:` follow-up in `notes` for the banker instead.

- `AI-SEARCHABLE` Local business journals, newspapers, chamber pages, and award lists
- `AI-SEARCHABLE` Company websites, leadership pages, acquisition announcements, expansion news
- `AI-SEARCHABLE` Oklahoma Department of Commerce data, employer, and expansion pages
- `AI-SEARCHABLE` Local economic development organizations and industrial park pages
- `HUMAN-PULL` Oklahoma Secretary of State business entity search portal
- `HUMAN-PULL` Oklahoma Corporation Commission oil and gas portals and operator databases
- `HUMAN-PULL` County assessor and county clerk record portals

## Oklahoma search patterns

Use town, county, and region names together. Many Oklahoma businesses serve from a nearby city even when the owner lives in a smaller town. Sector-specific query shapes live in the sector files; region-level shapes:

```text
[county] Oklahoma largest employers private company
[town] Oklahoma business sold acquired
[town] Oklahoma family owned company anniversary
[county] Oklahoma ranch land auction family
```

## Unturned Stones (high-alpha public databases)

These find the quiet $10M winner competitors miss. Work 2-3 of them into every run — especially when standard searches return the same names competitors already know. One or two searches each, then move on.

- PPP loan data (ProPublica Tracker / SBA release): loan size is a payroll-scale proxy for private companies. Query: `"[company]" PPP loan` or `[town] Oklahoma largest PPP loans`. `AI-SEARCHABLE`
- FEC individual contributions: repeat $5K+ political donors self-identify as liquid. Best route: fetch `city-data.com/elec2/elec-[TOWN]-OK.html` directly — name + employer + occupation + amounts on one page (proven top producer, 2026-07 O&G run). `AI-SEARCHABLE`
- Form 990s (ProPublica Nonprofit Explorer): private family foundations and hospital/school donor boards by city — wealthy families with no operating-company footprint. Query: `[town] Oklahoma family foundation 990`. `AI-SEARCHABLE`
- OSCN (oscn.net) Oklahoma court records: probate, estates, guardianships, royalty litigation — wealth-transfer events by county. Search names found elsewhere against OSCN; browsing raw dockets is `HUMAN-PULL`.
- EWG Farm Subsidy Database: largest USDA subsidy recipients by county roughly equal largest land families. Query: `[county] Oklahoma farm subsidy top recipients`. NOTE: the top-recipient tables themselves are JS-gated — direct fetch returns an empty shell, so use search snippets only; table browsing is `HUMAN-PULL`.
- FAA aircraft registry: private aircraft registered to OK towns/LLCs signal $5M+ owners. Query: `[town] Oklahoma registered aircraft owner`. `AI-SEARCHABLE`
- State incentive award lists (Quality Jobs program, TIF announcements): private companies big enough to win incentives. `AI-SEARCHABLE`
- Land/equipment auction results and estate sale coverage: `[county] Oklahoma ranch sold auction acres`. `AI-SEARCHABLE`
- Obituaries of business owners/ranchers (already in the O&G file): surviving spouse/children inherit — pair with OSCN probate for confirmation. `AI-SEARCHABLE`

## Ranking guidance

Highest ranks usually come from:

- Private company owners with clear scale
- Recent sale, acquisition, expansion, or liquidity event
- Multi-location practice or franchise owners
- Oilfield service, trucking, disposal, fabrication, or equipment businesses
- Large land/ranch/mineral families when public sources connect the name clearly

Lower ranks usually include:

- Single-location professionals with no clear ownership scale
- Branch managers of national companies
- Public-company executives who are likely already banked
- Names where identity or ownership is not verifiable

## Refresh rhythm

For refreshes, look for changes since `last_checked` in the cache. Do not redo the whole web unless the cache is empty or stale. Three months is a normal refresh interval.
