"""
Canned Oklahoma sample used when no ANTHROPIC_API_KEY is set, so the whole
click-to-Excel flow works for free before you go live. These are real
public-record rows already in your cache -- not invented. Once you add an API
key, server.py runs the live agent instead of this.
"""

DEMO_ROWS = [
    {
        "rank": "1", "name": "John Linton", "city_county": "Tonkawa, Kay County OK",
        "sector": "Oil & Gas / Royalties", "role_type": "Co-owner",
        "business": "Co-founder, O-K Bit Service Inc (rerun drill bits)",
        "wealth_signal": "50+ yr founder-owned niche oilfield supplier, 3 locations, world's largest rerun-bit retailer",
        "source_label": "O-K Bit About page", "source_url": "https://okbit.com/about/",
        "confidence": "High",
        "why_fit": "Closely-held 50-yr owner, national reach, classic quiet wealth",
        "hook": "Multi-generation succession / wealth-transfer opening",
        "notes": "", "more_available_count": "2",
        "more_available_note": "Brother Jim + next-gen sons also owners",
    },
    {
        "rank": "2", "name": "Jim Linton", "city_county": "Tonkawa, Kay County OK",
        "sector": "Oil & Gas / Royalties", "role_type": "Co-owner",
        "business": "Co-founder, O-K Bit Service Inc",
        "wealth_signal": "Co-founded 1973; company now spans 3 states, stocks 25,000+ bits",
        "source_label": "O-K Bit About page", "source_url": "https://okbit.com/about/",
        "confidence": "High", "why_fit": "Co-founder of same 50-yr family company",
        "hook": "Same succession angle as brother John",
        "notes": "", "more_available_count": "", "more_available_note": "",
    },
    {
        "rank": "3", "name": "Brad Barby", "city_county": "Woodward, Woodward County OK",
        "sector": "Oil & Gas / Royalties", "role_type": "Owner",
        "business": "President/owner, Latigo Oil & Gas Inc",
        "wealth_signal": "~#60 Oklahoma producer, roughly 50 wells",
        "source_label": "D&B profile",
        "source_url": "https://www.dnb.com/business-directory/company-profiles.latigo_oil__gas_inc.html",
        "confidence": "High", "why_fit": "Owner-operated producer with clear scale",
        "hook": "Operator liquidity / royalty planning",
        "notes": "", "more_available_count": "", "more_available_note": "",
    },
    {
        "rank": "4", "name": "Stanley Barby", "city_county": "Beaver, Beaver County OK",
        "sector": "Oil & Gas / Royalties", "role_type": "Owner",
        "business": "Owner, Bar B Ranch",
        "wealth_signal": "45,000-acre ranch plus oil & gas interests",
        "source_label": "AQHA Bar B Ranch", "source_url": "https://www.aqha.com/-/bar-b-ranch",
        "confidence": "Med-High", "why_fit": "Large land + mineral family",
        "hook": "Land/mineral estate and legacy planning",
        "notes": "", "more_available_count": "", "more_available_note": "",
    },
    {
        "rank": "5", "name": "Steve Nightingale", "city_county": "Fairview, Major County OK",
        "sector": "Oil & Gas / Royalties", "role_type": "Co-owner",
        "business": "Co-owner, Major Gas Company (propane distributor)",
        "wealth_signal": "30-year regional propane distributor",
        "source_label": "Major Gas Company", "source_url": "https://majorgascompany.com/",
        "confidence": "Med-High", "why_fit": "Long-held distributor, under-banked",
        "hook": "Owner-operator retirement / sale readiness",
        "notes": "", "more_available_count": "", "more_available_note": "",
    },
    {
        "rank": "6", "name": "Owner not publicly identified",
        "city_county": "Ponca City, Kay County OK",
        "sector": "Oil & Gas / Royalties", "role_type": "Owner",
        "business": "Owner, RK Oilfield Services LLC (heavy hauling / crane)",
        "wealth_signal": "20-year multi-service oilfield fleet, active since 2005",
        "source_label": "RK Oilfield Services", "source_url": "https://www.rkoilfield.com/",
        "confidence": "Low",
        "why_fit": "Established closely-held operator once owner is named",
        "hook": "Under-banked operator; identify principal first",
        "notes": "FLAG: owner name not public; needs OK Secretary of State officer pull",
        "more_available_count": "", "more_available_note": "",
    },
]
