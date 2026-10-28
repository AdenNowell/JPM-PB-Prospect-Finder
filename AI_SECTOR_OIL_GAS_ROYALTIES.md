# AI Sector Rules - Oil & Gas / Royalties

Use this file for oilfield services, midstream-adjacent private companies, royalty/mineral families, landowners with mineral signals, disposal, trucking, equipment, and Oklahoma energy wealth.

Depth protocol: see `AI_BASE_RULES.md` (owner-only by default, 3-name cap, `role_type` required).

## Target profile

Prioritize nameable private wealth:

- Oilfield service company owners
- Water hauling, trucking, disposal, saltwater, roustabout, pipeline, and equipment owners
- Private midstream or energy infrastructure contractors
- Fabricators and suppliers serving energy companies
- Royalty/mineral owners only when public records or news clearly identify the person/family
- Land/ranch families with public mineral, lease, estate, or sale signals

## High-yield sources

- Company websites and leadership/history pages
- Oklahoma Secretary of State entity search
- Oklahoma Corporation Commission data and operator records
- County clerk, assessor, land, and court records when accessible
- Local obituaries for oilman/rancher/business-owner wealth-transfer context
- News about acquisitions, land/mineral sales, lawsuits, bankruptcy claims, or estate activity
- Trade association, chamber, and award pages
- FMCSA SAFER carrier snapshots: power-unit and driver counts show fleet scale for trucking, hauling, and disposal owners. Query: `"[company]" FMCSA SAFER power units` or `[town] Oklahoma oilfield trucking FMCSA`
- PPP loan data (ProPublica): payroll-scale proxy for service companies. Query: `"[company]" PPP loan`
- OSCN (oscn.net): royalty litigation, probate, and estate cases connect names to mineral wealth. Search names found elsewhere; raw docket browsing is HUMAN-PULL.

## Advanced sources (work 3-5 of these into EVERY O&G run)

These outproduce generic `[town] oilfield owner` queries. Use them first; fall back to basic search patterns only to fill gaps.

- **Operator/well databases (DrillingEdge, ShaleXP, wellsdatabase mirrors of OCC data):** rank private operators by county with well counts and production. Small private operator with 20-200 wells = ideal quiet wealth. Query: `drillingedge [county] Oklahoma top operators` or `shalexp "[company]" Oklahoma production`. `AI-SEARCHABLE`. The OCC OAP portal itself is `HUMAN-PULL`.
- **E&P bankruptcy claims registers (Kroll, Stretto, Epiq, Omni):** creditor matrices in Chesapeake/SandRidge/Chaparral/White Star-type cases list royalty and working-interest owners by name and county — public, indexed, and nobody prospects them. Query: `"[county]" royalty owner claim [operator] bankruptcy` or search names found elsewhere against `kccllc OR stretto "[name]"`. `AI-SEARCHABLE`
- **Deal trade press (Hart Energy, Shale Experts, PLS, Oil & Gas Journal, World Oil, natural gas intel):** asset sales and private-operator acquisitions name selling families. Query: `[basin/county] Oklahoma acquisition private operator Hart Energy` or `"[company]" sells Oklahoma assets`. `AI-SEARCHABLE`
- **SEC filings of public acquirers (8-K, 10-K property sections, press releases):** public buyers name the private sellers of Oklahoma assets. Query: `SEC 8-K acquisition "[county] County, Oklahoma"`. `AI-SEARCHABLE`
- **Mineral/royalty auction results (EnergyNet, Oil & Gas Asset Clearinghouse):** lot descriptions and seller trusts by county signal recent mineral liquidity. Query: `EnergyNet [county] Oklahoma minerals sold`. `AI-SEARCHABLE`
- **NARO (National Association of Royalty Owners) Oklahoma chapter:** officers, convention speakers, and award pages are self-identified royalty owners. Query: `NARO Oklahoma chapter officers [name/town]`. `AI-SEARCHABLE`
- **Petroleum Alliance of Oklahoma (formerly OIPA/OKOGA) + Oklahoma Energy Resources Board:** member spotlights, board lists, Wildcatter awards name private operators. Skip anyone famous. `AI-SEARCHABLE`
- **okcountyrecords.com (county clerk ROD index):** mineral deeds, oil & gas leases by grantor/grantee. Verification of names found elsewhere is `AI-SEARCHABLE` via web index; systematic browsing is `HUMAN-PULL`.
- **Baker Hughes rig counts + OCC drilling permits by county:** identifies which private operators are actively drilling (spending $3M+/well = capital depth). Query: `[county] Oklahoma drilling permits [year] operator`. `AI-SEARCHABLE`
- **Oklahoma Tax Commission gross production / PUN records:** `HUMAN-PULL` — flag in notes when a name needs production-scale confirmation.
- **FEC donors by town (city-data.com):** fetch `city-data.com/elec2/elec-[TOWN]-OK.html` directly — one page lists donor name + employer + occupation + amounts. Best single owner-name source proven for small oilfield towns (2026-07 run: ~10 qualified names in one fetch). Repeat $1k+ donors with O&G/ranch occupations are liquid and self-identified. `AI-SEARCHABLE`
- **WARNING — mineralholders.com:** its appraised values cover TEXAS properties only. Oklahoma royalty owners show misleadingly tiny values there. Use it for names and interest counts only, never for wealth sizing.

## Owner-name resolution ladder

Company discovery is cheap (ShaleXP, PPP); attaching an owner NAME is the bottleneck because OK SOS officer lookup is `HUMAN-PULL`. Work this ladder, max ~2 tries per rung, then FLAG and move on:

1. Company website About/Team/history page.
2. FEC town page on city-data (above) — match the company name or occupation.
3. News, chamber, BBB, or trade-directory listings naming a principal.
4. PPP/FMCSA confirm SCALE but never ownership — do not infer an owner from them alone.
5. Still no name → write `FLAG: owner needs OK SOS officer pull` in notes. Batch every SOS flag into one list for the banker at end of run.

## Search patterns

```text
[town] Oklahoma oilfield service owner
[county] Oklahoma saltwater disposal owner
[town] Oklahoma trucking oilfield owner
[town] Oklahoma roustabout owner
[county] Oklahoma mineral owner family
[county] Oklahoma oilman rancher obituary
[company name] Oklahoma oilfield owner founder
[company name] Oklahoma acquisition sale
```

## Important dead-end rule

Do not spend the run trying to fully identify individual mineral owners from open web search. Many are hidden behind LLCs, trusts, probate records, or paywalled mineral datasets.

After about 2 weak tries, stop and write a records-level gap in `notes`, such as:

```text
FLAG: Mineral ownership likely requires county clerk/assessor plus minerals-data pull.
```

## Include when

Include a prospect when public sources connect the person to a private energy-related company, land/mineral signal, sale, estate, or scale marker.

For second/third-order depth, apply the depth-signal test in `AI_BASE_RULES.md`. For royalty/mineral or ranch families, do not force extra names unless public records or news clearly identify co-owners, partners, trustees, or Director-level-or-above operators.

## Avoid or downgrade

- Major public-company executives unless the user asks for them
- Nationally famous names likely already covered by private banks
- Pure LLC names with no reliable person attached
- Royalty/mineral guesses with no public identity connection
- Titles below Director unless the person is separately verified as owner, founder, co-owner, partner, trustee, or equity holder
