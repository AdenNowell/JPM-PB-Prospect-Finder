# AI Sector Rules - Healthcare

Use this file for independent healthcare, dental, veterinary, pharmacy, outpatient clinic, and practice-owner prospecting.

Depth protocol: see `AI_BASE_RULES.md` (owner-only by default, 3-name cap, `role_type` required).

## Target profile

Prioritize owner-led or partner-led practices with scale:

- Dental groups, oral surgery, orthodontics, and specialty practices
- Veterinary clinics and multi-location animal hospitals
- Independent pharmacies and compounding pharmacies
- Physician-owned specialty clinics
- Surgery centers, imaging centers, physical therapy groups, and urgent care groups
- Practice sellers or owners involved in recent acquisitions

## High-yield sources

- Practice websites, "About", "Team", "Locations", and "History" pages
- State license verification pages when needed to confirm professional identity
- Secretary of State entity records for practice ownership clues
- Acquisition, partnership, private equity, or DSO/MSO announcements
- Local "best of", chamber, health system partner, and community award pages
- Commercial real estate and facility expansion news when tied to the practice
- CMS/NPPES NPI registry and Medicare provider data: confirms practice ownership/organization structure and billing scale. Query: `"[practice name]" NPI organization owner` or `[town] Oklahoma Medicare provider [specialty]`
- PPP loan data (ProPublica): practice loan size proxies staff size. Query: `"[practice name]" PPP loan`
- Practice sellers to DSO/PE groups: fresh liquidity, rarely prospected. Query: `[town] Oklahoma dental practice acquired DSO`

## Search patterns

```text
[town] Oklahoma dental practice owner
[town] Oklahoma oral surgery owner
[town] Oklahoma veterinary clinic owner
[town] Oklahoma independent pharmacy owner
[town] Oklahoma physician clinic founder
[practice name] Oklahoma owner founder
[practice name] acquisition Oklahoma
[county] Oklahoma multi location dental veterinary pharmacy
```

## Include when

Include a prospect when the person is publicly connected to ownership, founding, partnership, sale, or multi-location scale.

Good signals include multiple locations, specialty practice ownership, acquisition, facility expansion, independent pharmacy ownership, or long-tenured owner/operator status.

For second/third-order depth, apply the depth-signal test in `AI_BASE_RULES.md`. Exclude ordinary associate providers unless ownership, partnership, or Director-level-or-above seniority is publicly clear.

## Avoid or downgrade

- Employee providers with no ownership signal
- Hospital-employed physicians unless there is a separate private ownership signal
- Large health-system executives likely already covered
- Profile pages that identify only clinical role and no business ownership
- Office managers, practice managers, associates, and other titles below Director unless ownership/equity is verified
