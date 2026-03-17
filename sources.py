# ─────────────────────────────────────────────────────────────
# DNNK Overvågningskilder – komplet liste
# Opdater denne fil når nye medlemmer tilføjes
# ─────────────────────────────────────────────────────────────

# ── NYHEDSMEDIER & FAGBLADE ──
RSS_NEWS = {
    "Ingeniøren":           "https://ing.dk/rss/alle",
    "Altinget Miljø":       "https://www.altinget.dk/miljoe/rss.aspx",
    "Teknik & Miljø":       "https://www.tm.dk/rss",
    "DR Nyheder":           "https://www.dr.dk/nyheder/service/feeds/allenyheder",
    "TV2 Nyheder":          "https://feeds.tv2.dk/nyheder/rss",
    "Politiken":            "https://politiken.dk/rss/senestenyt.rss",
    "Politiken Klima":      "https://politiken.dk/rss/klima.rss",
    "Berlingske":           "https://www.berlingske.dk/rss/nyheder/nyheder.rss",
    "Klimamonitor":         "https://klimamonitor.dk/feed/",
}

# ── VIDENSINSTITUTIONER ──
RSS_VIDEN = {
    "DMI":                  "https://www.dmi.dk/rss/",
    "GEUS":                 "https://www.geus.dk/rss",
    "DTU":                  "https://www.dtu.dk/service/nyhedsliste/rss",
    "Aarhus Universitet":   "https://news.au.dk/rss.aspx",
    "KU":                   "https://www.ku.dk/nyheder/rss/",
    "SDU":                  "https://www.sdu.dk/rss",
    "Klimatilpasning.dk":   "https://klimatilpasning.dk/feed/",
    "Klimatorium":          "https://klimatorium.dk/feed/",
    "IDA":                  "https://ida.dk/rss",
    "DCCC":                 "https://www.dmi.dk/klima/klimaforandringer/rss/",
}

# ── MYNDIGHEDER & MINISTERIER ──
RSS_MYNDIGHEDER = {
    "Miljøstyrelsen":       "https://mst.dk/service/nyheder/rss",
    "Miljøministeriet":     "https://www.mim.dk/rss",
    "Energistyrelsen":      "https://ens.dk/service/nyheder/rss",
    "Kystdirektoratet":     "https://kyst.dk/rss",
    "SDFE":                 "https://sdfe.dk/rss",
    "KL":                   "https://www.kl.dk/rss/",
    "Klimarådet":           "https://klimaraadet.dk/da/rss.xml",
    "Erhvervsstyrelsen":    "https://erhvervsstyrelsen.dk/rss",
}

# ── DNNK-MEDLEMMER: RÅDGIVERE & VIRKSOMHEDER ──
RSS_RAADGIVERE = {
    "Rambøll":              "https://ramboll.com/rss",
    "COWI":                 "https://www.cowi.com/rss",
    "Sweco":                "https://www.sweco.dk/rss",
    "NIRAS":                "https://www.niras.dk/rss",
    "WSP":                  "https://www.wsp.com/rss",
    "Krüger / Veolia":      "https://www.kruger.dk/rss",
    "Orbicon / WSP":        "https://www.wsp.com/da-dk/rss",
    "Jacobs":               "https://www.jacobs.com/rss",
    "Atkins":               "https://www.atkinsglobal.com/rss",
    "Teknologisk Institut": "https://www.teknologisk.dk/rss",
    "Schønherr":            "https://www.schonherr.dk/feed/",
    "SLA Architects":       "https://www.sla.dk/feed/",
    "Hasløv & Kjærsgaard":  "https://www.hkarkitekter.dk/feed/",
}

# ── DNNK-MEDLEMMER: FORSYNINGER ──
RSS_FORSYNINGER = {
    "HOFOR":                "https://www.hofor.dk/rss",
    "VandCenter Syd":       "https://vandcenter.dk/rss",
    "Aarhus Vand":          "https://aarhusvand.dk/rss",
    "Novafos":              "https://novafos.dk/feed/",
    "Nordvand":             "https://nordvand.dk/feed/",
    "Frederiksberg Fors.":  "https://frb-forsyning.dk/rss",
    "Hillerød Forsyning":   "https://hfors.dk/rss",
    "BIOFOS":               "https://www.biofos.dk/rss",
    "Odense Renovation":    "https://www.odenserenovation.dk/rss",
    "Danva":                "https://www.danva.dk/nyheder/rss",
}

# ── DNNK-MEDLEMMER: KOMMUNER (udvalgte med aktiv klimatilpasning) ──
RSS_KOMMUNER = {
    "Kbh. Kommune":         "https://www.kk.dk/rss",
    "Aarhus Kommune":       "https://www.aarhus.dk/rss/",
    "Odense Kommune":       "https://www.odense.dk/rss",
    "Frederiksberg":        "https://www.frederiksberg.dk/rss",
    "Aalborg Kommune":      "https://www.aalborg.dk/rss",
    "Vejle Kommune":        "https://www.vejle.dk/rss",
    "Roskilde Kommune":     "https://roskilde.dk/rss",
    "Helsingør Kommune":    "https://www.helsingor.dk/rss",
    "Næstved Kommune":      "https://www.naestved.dk/rss",
    "Holstebro Kommune":    "https://www.holstebro.dk/rss",
}

# ── EU & INTERNATIONALE ──
RSS_EU = {
    "EU Kommissionen":      "https://ec.europa.eu/environment/rss_en.xml",
    "EEA":                  "https://www.eea.europa.eu/rss",
    "Climate-ADAPT":        "https://climate-adapt.eea.europa.eu/rss",
}

# ── SAMLET DICTIONARY pr. kategori ──
ALLE_FEEDS = {
    "Nyheder & fagblade":   RSS_NEWS,
    "Vidensinstitutioner":  RSS_VIDEN,
    "Myndigheder":          RSS_MYNDIGHEDER,
    "Rådgivere":            RSS_RAADGIVERE,
    "Forsyninger":          RSS_FORSYNINGER,
    "Kommuner":             RSS_KOMMUNER,
    "EU & Internationalt":  RSS_EU,
}

# Flad liste til RSS-scanning
ALL_FEEDS_FLAT = {}
for gruppe, feeds in ALLE_FEEDS.items():
    for navn, url in feeds.items():
        ALL_FEEDS_FLAT[navn] = {"url": url, "gruppe": gruppe}


# ─────────────────────────────────────────────────────────────
# NORDISKE NABOER – vidensinstitutioner og medier
# ─────────────────────────────────────────────────────────────
RSS_NORDEN = {
    # Sverige
    "SMHI (Sverige)":           "https://www.smhi.se/rss/nyheter.xml",
    "Naturvårdsverket (SE)":    "https://www.naturvardsverket.se/rss/nyheter.rss",
    "SVT Nyheder Klima":        "https://www.svt.se/nyheter/rss.xml",
    "Havs- och vattenmyndigh.": "https://www.havochvatten.se/rss",
    "VA-guiden (SE)":           "https://www.vaguiden.se/rss",
    "Svenskt Vatten":           "https://www.svensktvatten.se/rss",
    "SEI Stockholm":            "https://www.sei.org/rss",

    # Norge
    "NVE (Norge)":              "https://www.nve.no/rss/nyheter/",
    "Miljødirektoratet (NO)":   "https://www.miljodirektoratet.no/rss/",
    "NRK Klima":                "https://www.nrk.no/klima/rss.xml",
    "Cicero (NO)":              "https://cicero.oslo.no/rss",
    "NCCS Norge":               "https://www.nccs.no/rss",

    # Finland
    "SYKE (Finland)":           "https://www.syke.fi/rss",
    "Ilmatieteen laitos (FI)":  "https://www.ilmatieteenlaitos.fi/rss",
    "YLE Nyheder Klimat":       "https://feeds.yle.fi/uutiset/v1/majorHeadlines/YLE_UUTISET.rss",

    # Island & Færøerne
    "Veðurstofa Íslands":       "https://en.vedur.is/rss/",

    # Nordisk samarbejde
    "Nordisk Råd":              "https://www.norden.org/da/rss.xml",
    "Nordic Climate Group":     "https://www.sei.org/rss",
    "C2C CC (Coast2Coast)":     "https://www.c2ccc.eu/feed/",
}

# ─────────────────────────────────────────────────────────────
# EU PROJEKTDATABASER – live feeds og API-endpoints
# ─────────────────────────────────────────────────────────────
RSS_EU_PROJEKTER = {
    # Climate-ADAPT – EEA's officielle klimatilpasningsplatform
    "Climate-ADAPT Nyheder":    "https://climate-adapt.eea.europa.eu/en/rss",
    "Climate-ADAPT Cases":      "https://climate-adapt.eea.europa.eu/en/knowledge/adaptation-case-studies/rss",
    "EEA Nyheder":              "https://www.eea.europa.eu/highlights/rss",

    # Interreg – transnationalt samarbejde (BSR inkl. DK)
    "Interreg Baltic Sea":      "https://interreg-baltic.eu/feed/",
    "Interreg North Sea":       "https://northsearegion.eu/feed/",
    "Interreg Europe":          "https://www.interregeurope.eu/rss",
    "Interreg Central Europe":  "https://www.interreg-central.eu/feed/",

    # LIFE-programmet – EU's miljøfond
    "LIFE Programme":           "https://cinea.ec.europa.eu/rss/life",

    # Horizon Europe / CORDIS
    "CORDIS Klimaprojekter":    "https://cordis.europa.eu/rss/projects/climate-adaptation",
    "EU Kommissionen Klima":    "https://ec.europa.eu/clima/rss_en.xml",

    # Copernicus klimatjenester
    "Copernicus C3S":           "https://climate.copernicus.eu/rss",
    "Copernicus ECMWF":         "https://www.ecmwf.int/rss",

    # European Environment Agency
    "EEA Klimaindikatorer":     "https://www.eea.europa.eu/themes/climate/rss",

    # Mission Adaptation (EU's klimamission)
    "Mission Clima EU":         "https://research-and-innovation.ec.europa.eu/rss",
}

# ─────────────────────────────────────────────────────────────
# Tilføj til ALLE_FEEDS
# ─────────────────────────────────────────────────────────────
ALLE_FEEDS["Nordiske naboer"] = RSS_NORDEN
ALLE_FEEDS["EU projekter"] = RSS_EU_PROJEKTER

# Genbyg flad liste
ALL_FEEDS_FLAT.clear()
for gruppe, feeds in ALLE_FEEDS.items():
    for navn, url in feeds.items():
        ALL_FEEDS_FLAT[navn] = {"url": url, "gruppe": gruppe}


# ─────────────────────────────────────────────────────────────
# FORSIKRING & FINANS – skadedata og klimarisiko
# ─────────────────────────────────────────────────────────────
RSS_FORSIKRING = {
    "Forsikring & Pension":     "https://www.forsikringogpension.dk/rss",
    "Realdania":                "https://realdania.dk/rss",
    "Villum Fonden":            "https://villumfonden.dk/rss",
    "Velux Fonden":             "https://veluxfoundations.dk/rss",
    "Landsbyggefonden":         "https://www.landsbyggefonden.dk/rss",
    "Tryg Fonden":              "https://www.trygfonden.dk/rss",
}

# ─────────────────────────────────────────────────────────────
# TEKNOLOGI & LØSNINGSLEVERANDØRER
# ─────────────────────────────────────────────────────────────
RSS_TEKNOLOGI = {
    "DHI":                      "https://www.dhigroup.com/rss",
    "Grundfos":                 "https://www.grundfos.com/rss",
    "Wavin":                    "https://www.wavin.com/rss",
    "SCALGO":                   "https://scalgo.com/rss",
    "Krüger / Veolia DK":       "https://www.kruger.dk/rss",
    "Xylem Water":              "https://www.xylem.com/rss",
    "Kamstrup":                 "https://www.kamstrup.com/rss",
    "AVK":                      "https://www.avk.dk/rss",
}

# ─────────────────────────────────────────────────────────────
# DANSKE PLATFORME & NETVÆRK
# ─────────────────────────────────────────────────────────────
RSS_PLATFORME = {
    "State of Green":           "https://stateofgreen.com/rss",
    "BLOXHUB":                  "https://bloxhub.org/rss",
    "Gate 21":                  "https://www.gate21.dk/rss",
    "Klimatorium Lemvig":       "https://klimatorium.dk/feed/",
    "Vand i Byer":              "https://www.vandibyer.dk/rss",
    "KLIKOVAND":                "https://www.klikovand.dk/rss",
    "C2C CC (Coast2Coast)":     "https://www.c2ccc.eu/feed/",
    "Urban Futures Centre":     "https://urbanfuturescentre.dk/rss",
    "BLÅ GRØN":                 "https://blaagron.dk/feed/",
}

# ─────────────────────────────────────────────────────────────
# REGIONER – undervurderede aktører i klimatilpasning
# ─────────────────────────────────────────────────────────────
RSS_REGIONER = {
    "Region Midtjylland":       "https://www.rm.dk/rss",
    "Region Nordjylland":       "https://rn.dk/rss",
    "Region Syddanmark":        "https://www.rsyd.dk/rss",
    "Region Sjælland":          "https://www.regionsjaelland.dk/rss",
    "Region Hovedstaden":       "https://www.regionh.dk/rss",
}

# ─────────────────────────────────────────────────────────────
# JURIDISK & REGULERING – love, bekendtgørelser, EU-direktiver
# ─────────────────────────────────────────────────────────────
RSS_REGULERING = {
    "Retsinformation":          "https://www.retsinformation.dk/rss",
    "Høringsportalen":          "https://hoeringsportalen.dk/rss",
    "Stormrådet":               "https://www.stormraadet.dk/rss",
    "Kystdirektoratet":         "https://kyst.dk/rss",
    "Forsyningstilsynet":       "https://forsyningstilsynet.dk/rss",
    "Konkurrence- og Forbrug":  "https://www.kfst.dk/rss",
    "EUR-Lex (DK klima)":       "https://eur-lex.europa.eu/rss/rss.xml?type=act&subject=15&language=da",
}

# ─────────────────────────────────────────────────────────────
# INTERNATIONALE VIDENSINSTITUTIONER
# ─────────────────────────────────────────────────────────────
RSS_INTERNATIONAL = {
    "NIVA (Norge)":             "https://www.niva.no/rss",
    "IWA (Int. Water Assoc.)":  "https://iwa-network.org/rss",
    "WaterWorld":               "https://www.waterworld.com/rss",
    "FloodList":                "https://floodlist.com/feed",
    "The Water Network":        "https://thewaternetwork.com/rss",
    "Global Water Intelligence": "https://www.globalwaterintel.com/rss",
    "IPCC Nyheder":             "https://www.ipcc.ch/rss",
    "UN Environment":           "https://www.unep.org/rss.xml",
    "World Resources Institute": "https://www.wri.org/rss.xml",
    "C40 Cities":               "https://www.c40.org/rss",
    "ICLEI":                    "https://iclei.org/rss",
    "Deltares":                 "https://www.deltares.nl/rss",
    "Stockholm Environment Inst.": "https://www.sei.org/rss",
}

# ─────────────────────────────────────────────────────────────
# DANSKE FAGMEDIER & BRANCHEORGANISATIONER
# ─────────────────────────────────────────────────────────────
RSS_FAG = {
    "Byplan Nyt":               "https://byplannyt.dk/feed/",
    "Landinspektøren":          "https://www.landinspektoeren.dk/rss",
    "Stads og Havneingeniøren": "https://www.shi.dk/rss",
    "Byggeri København":        "https://byggericopenhagen.dk/rss",
    "Arkitektens Forlag":       "https://www.arkfo.dk/rss",
    "Landscape Architecture":   "https://www.landscapearchitecturemagazine.org/rss",
    "KL Teknik & Miljø":        "https://www.kl.dk/fagomraader/teknik-og-miljo/rss/",
    "DANVA Nyheder":            "https://www.danva.dk/nyheder/rss",
    "Dansk Vand Konference":    "https://danskvandk.dk/rss",
}

# ─────────────────────────────────────────────────────────────
# Tilføj alle nye grupper til ALLE_FEEDS
# ─────────────────────────────────────────────────────────────
ALLE_FEEDS["Forsikring & finans"] = RSS_FORSIKRING
ALLE_FEEDS["Teknologi & leverandører"] = RSS_TEKNOLOGI
ALLE_FEEDS["Platforme & netværk"] = RSS_PLATFORME
ALLE_FEEDS["Regioner"] = RSS_REGIONER
ALLE_FEEDS["Regulering & jura"] = RSS_REGULERING
ALLE_FEEDS["Internationale inst."] = RSS_INTERNATIONAL
ALLE_FEEDS["Fagmedier"] = RSS_FAG

# Genbyg flad liste
ALL_FEEDS_FLAT.clear()
for gruppe, feeds in ALLE_FEEDS.items():
    for navn, url in feeds.items():
        ALL_FEEDS_FLAT[navn] = {"url": url, "gruppe": gruppe}
