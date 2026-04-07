# ─────────────────────────────────────────────────────────────
# DNNK Overvågningskilder – bekræftet fungerende
# Sidst testet: 2026-04-07 (19 virker bekræftet)
# ─────────────────────────────────────────────────────────────

# ── NYHEDER & FAGBLADE ──
RSS_NEWS = {
    "Ingeniøren":               "https://ing.dk/rss",
    "Ingeniøren Energi & Miljø":"https://ing.dk/term/rss/1964",
    "Altinget Miljø":           "https://www.altinget.dk/miljoe/rss.aspx",
    "DR Nyheder":               "https://www.dr.dk/nyheder/service/feeds/allenyheder",
}

# ── VIDENSINSTITUTIONER ──
RSS_VIDEN = {
    "IDA":                      "https://ida.dk/rss",
}

# ── RÅDGIVERE ──
RSS_RAADGIVERE = {
    "Sweco":                    "https://www.sweco.dk/rss",
}

# ── FORSYNINGER ──
RSS_FORSYNINGER = {
    "HOFOR":                    "https://www.hofor.dk/rss",
}

# ── NORDISKE NABOER ──
RSS_NORDEN = {
    "SVT Nyheder Klima":        "https://www.svt.se/nyheter/rss.xml",
    "VA-guiden (SE)":           "https://www.vaguiden.se/rss",
    "NCCS Norge":               "https://www.nccs.no/rss",
    "NRK Klima":                "https://www.nrk.no/toppsaker.rss",
}

# ── EU PROJEKTER ──
RSS_EU_PROJEKTER = {
    "Interreg Baltic Sea":      "https://interreg-baltic.eu/feed/",
}

# ── PLATFORME & NETVÆRK ──
RSS_PLATFORME = {
    "Klimatorium":              "https://klimatorium.dk/feed/",
    "BLOXHUB":                  "https://bloxhub.org/rss",
    "Gate 21":                  "https://www.gate21.dk/rss",
    "Vand i Byer":              "https://www.vandibyer.dk/rss",
    "State of Green":           "https://stateofgreen.com/en/feed/",
}

# ── INTERNATIONALE INSTITUTIONER ──
RSS_INTERNATIONAL = {
    "FloodList":                "https://floodlist.com/feed",
    "ICLEI":                    "https://iclei.org/news/rss/",
    "UN Environment":           "https://www.unep.org/rss.xml",
}

# ─────────────────────────────────────────────────────────────
# SAMLET DICTIONARY
# ─────────────────────────────────────────────────────────────
ALLE_FEEDS = {
    "Nyheder & fagblade":       RSS_NEWS,
    "Vidensinstitutioner":      RSS_VIDEN,
    "Rådgivere":                RSS_RAADGIVERE,
    "Forsyninger":              RSS_FORSYNINGER,
    "Nordiske naboer":          RSS_NORDEN,
    "EU projekter":             RSS_EU_PROJEKTER,
    "Platforme & netværk":      RSS_PLATFORME,
    "Internationale inst.":     RSS_INTERNATIONAL,
}

# Flad liste til scanning
ALL_FEEDS_FLAT = {}
for gruppe, feeds in ALLE_FEEDS.items():
    for navn, url in feeds.items():
        ALL_FEEDS_FLAT[navn] = {"url": url, "gruppe": gruppe}
