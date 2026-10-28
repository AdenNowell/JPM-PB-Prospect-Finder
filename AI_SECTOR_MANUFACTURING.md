# AI Sector Rules - Manufacturing / Industrial

Use this file when the target sector is manufacturing, industrial services, distribution, fabrication, logistics, or construction-adjacent owner-operators.

Depth protocol: see `AI_BASE_RULES.md` (owner-only by default, 3-name cap, `role_type` required).

## Target profile

Look for private, owner-led companies with signs of scale:

- Machine shops and metal fabrication
- Industrial equipment, oilfield equipment, or agricultural equipment manufacturers
- Specialty construction suppliers and contractors
- Plastics, packaging, food processing, HVAC, aerospace suppliers, and component makers
- Regional distributors with trucks, yards, warehouses, or multiple locations
- Family-owned companies with expansion news, incentives, awards, or long operating history

## High-yield sources

- Company "About", leadership, history, and news pages
- Oklahoma Commerce employer, expansion, and industry pages
- Local economic development organization pages
- Industrial park tenant lists
- Chamber business awards and manufacturer awards
- Secretary of State entity records to verify officers or registered agents
- News about expansions, new facilities, incentive awards, acquisitions, or plant investments
- PPP loan data (ProPublica/SBA): loan size proxies payroll scale for private companies with no public footprint. Query: `"[company]" PPP loan` or `[town] Oklahoma manufacturer largest PPP loan`
- SEC EDGAR Form D filings: private OK companies raising capital; names founders and executives. Query: `[company or town] Oklahoma Form D SEC`
- UCC filing coverage: heavy equipment financing signals fleet/plant scale. Query: `"[company]" Oklahoma UCC equipment`

## Search patterns

```text
[town] Oklahoma manufacturer owner founder
[county] Oklahoma manufacturers private company
[town] Oklahoma fabrication owner
[town] Oklahoma machine shop owner
[town] Oklahoma industrial services owner
[county] Oklahoma industrial park tenants
[company name] Oklahoma founder owner
[company name] Oklahoma expansion acquisition
```

## Include when

Include a person when there is a public connection between the person, the business, and the wealth signal.

Good signals include facility size, employee count, multiple locations, long-term ownership, acquisition/sale, large contracts, public expansion, or major equipment/fleet scale.

For second/third-order depth, apply the depth-signal test in `AI_BASE_RULES.md`. If signals are absent, mark the company owner-only and move on.

## Avoid or downgrade

- National public-company branches with no local owner
- Directory listings with no ownership or scale signal
- Companies that only share a town name but are headquartered elsewhere
- People named only as employees or plant managers unless ownership is clear
- Titles below Director unless the person is separately verified as owner, founder, co-owner, or equity partner
