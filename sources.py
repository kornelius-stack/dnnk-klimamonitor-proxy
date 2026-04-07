# ─────────────────────────────────────────────────────────────
# DNNK Overvågningskilder
# ─────────────────────────────────────────────────────────────

# ── BEKRÆFTEDE RSS FEEDS ──
RSS_NEWS = {
    "Ingeniøren":               "https://ing.dk/rss",
    "Ingeniøren Energi & Miljø":"https://ing.dk/term/rss/1964",
    "Altinget Miljø":           "https://www.altinget.dk/miljoe/rss.aspx",
    "DR Nyheder":               "https://www.dr.dk/nyheder/service/feeds/allenyheder",
}
RSS_VIDEN = {"IDA": "https://ida.dk/rss"}
RSS_RAADGIVERE = {"Sweco": "https://www.sweco.dk/rss"}
RSS_FORSYNINGER_RSS = {"HOFOR": "https://www.hofor.dk/rss"}
RSS_NORDEN = {
    "SVT Nyheder Klima":        "https://www.svt.se/nyheter/rss.xml",
    "VA-guiden (SE)":           "https://www.vaguiden.se/rss",
    "NCCS Norge":               "https://www.nccs.no/rss",
    "NRK Klima":                "https://www.nrk.no/toppsaker.rss",
}
RSS_EU = {"Interreg Baltic Sea": "https://interreg-baltic.eu/feed/"}
RSS_PLATFORME = {
    "Klimatorium":              "https://klimatorium.dk/feed/",
    "BLOXHUB":                  "https://bloxhub.org/rss",
    "Gate 21":                  "https://www.gate21.dk/rss",
    "Vand i Byer":              "https://www.vandibyer.dk/rss",
    "State of Green":           "https://stateofgreen.com/en/feed/",
}
RSS_INTERNATIONAL = {
    "FloodList":                "https://floodlist.com/feed",
    "ICLEI":                    "https://iclei.org/news/rss/",
    "UN Environment":           "https://www.unep.org/rss.xml",
}

ALLE_FEEDS = {
    "Nyheder & fagblade":       RSS_NEWS,
    "Vidensinstitutioner":      RSS_VIDEN,
    "Rådgivere":                RSS_RAADGIVERE,
    "Forsyninger":              RSS_FORSYNINGER_RSS,
    "Nordiske naboer":          RSS_NORDEN,
    "EU projekter":             RSS_EU,
    "Platforme & netværk":      RSS_PLATFORME,
    "Internationale inst.":     RSS_INTERNATIONAL,
}

ALL_FEEDS_FLAT = {}
for gruppe, feeds in ALLE_FEEDS.items():
    for navn, url in feeds.items():
        ALL_FEEDS_FLAT[navn] = {"url": url, "gruppe": gruppe}

# ─────────────────────────────────────────────────────────────
# SCRAPING — kommuner, forsyninger, styrelser, ministerier
# ─────────────────────────────────────────────────────────────

SCRAPE_SOURCES = {

    # ── MINISTERIER ──
    "Miljøministeriet":                 {"url": "https://www.mim.dk/nyheder/", "gruppe": "Myndigheder"},
    "Klima- og Energiministeriet":      {"url": "https://kefm.dk/aktuelt/nyheder/", "gruppe": "Myndigheder"},
    "Finansministeriet":                {"url": "https://www.fm.dk/nyheder/", "gruppe": "Myndigheder"},
    "Indenrigsministeriet":             {"url": "https://www.im.dk/nyheder/", "gruppe": "Myndigheder"},

    # ── STYRELSER & MYNDIGHEDER ──
    "Miljøstyrelsen":                   {"url": "https://mst.dk/nyheder/", "gruppe": "Myndigheder"},
    "Energistyrelsen":                  {"url": "https://ens.dk/nyheder/", "gruppe": "Myndigheder"},
    "Klimarådet":                       {"url": "https://klimaraadet.dk/da/nyheder", "gruppe": "Myndigheder"},
    "Kystdirektoratet":                 {"url": "https://kyst.dk/nyheder/", "gruppe": "Myndigheder"},
    "KL":                               {"url": "https://www.kl.dk/nyheder/", "gruppe": "Myndigheder"},
    "Naturstyrelsen":                   {"url": "https://naturstyrelsen.dk/nyheder/", "gruppe": "Myndigheder"},
    "Beredskabsstyrelsen":              {"url": "https://brs.dk/nyheder/", "gruppe": "Myndigheder"},
    "Forsyningstilsynet":               {"url": "https://forsyningstilsynet.dk/nyheder/", "gruppe": "Myndigheder"},
    "Stormrådet":                       {"url": "https://www.stormraadet.dk/nyheder/", "gruppe": "Myndigheder"},
    "Styrelsen for Dataforsyning":      {"url": "https://sdfe.dk/nyheder/", "gruppe": "Myndigheder"},
    "Vejdirektoratet":                  {"url": "https://www.vejdirektoratet.dk/nyheder", "gruppe": "Myndigheder"},
    "Statens Byggeforskningsinstitut":  {"url": "https://sbi.dk/nyheder/", "gruppe": "Myndigheder"},

    # ── FORSYNINGER – Storkøbenhavn ──
    "Nordvand":                         {"url": "https://nordvand.dk/nyheder/", "gruppe": "Forsyninger"},
    "Novafos":                          {"url": "https://novafos.dk/nyheder/", "gruppe": "Forsyninger"},
    "Frederiksberg Fors.":              {"url": "https://frb-forsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Hillerød Forsyning":               {"url": "https://hfors.dk/nyheder/", "gruppe": "Forsyninger"},
    "Køge Forsyning":                   {"url": "https://koegeforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Roskilde Forsyning":               {"url": "https://roskilde-forsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Greve Forsyning":                  {"url": "https://greveforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "SK Forsyning":                     {"url": "https://skforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "SAMN Forsyning":                   {"url": "https://samnforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "BIOFOS":                           {"url": "https://www.biofos.dk/nyheder/", "gruppe": "Forsyninger"},

    # ── FORSYNINGER – Østjylland ──
    "Aarhus Vand":                      {"url": "https://aarhusvand.dk/nyheder/", "gruppe": "Forsyninger"},
    "Skanderborg Forsyning":            {"url": "https://skanderborgforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Horsens Vand":                     {"url": "https://horsensvand.dk/nyheder/", "gruppe": "Forsyninger"},
    "Favrskov Forsyning":               {"url": "https://favrskovforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Randers Spildevand":               {"url": "https://randersspildevand.dk/nyheder/", "gruppe": "Forsyninger"},
    "Norddjurs Forsyning":              {"url": "https://norddjursforsyning.dk/nyheder/", "gruppe": "Forsyninger"},

    # ── FORSYNINGER – Midtjylland ──
    "Silkeborg Forsyning":              {"url": "https://silkeborgforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Herning Vand":                     {"url": "https://herningvand.dk/nyheder/", "gruppe": "Forsyninger"},
    "Viborg Vand":                      {"url": "https://viborgvand.dk/nyheder/", "gruppe": "Forsyninger"},
    "Holstebro Vand":                   {"url": "https://holstebrovand.dk/nyheder/", "gruppe": "Forsyninger"},
    "Ringkøbing-Skjern Fors.":          {"url": "https://rksk-forsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Lemvig Vand":                      {"url": "https://lemvigvand.dk/nyheder/", "gruppe": "Forsyninger"},
    "Struer Forsyning":                 {"url": "https://struerforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Ikast-Brande Spildevand":          {"url": "https://ibs-spildevand.dk/nyheder/", "gruppe": "Forsyninger"},

    # ── FORSYNINGER – Nordjylland ──
    "Aalborg Forsyning":                {"url": "https://www.aalborgforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Frederikshavn Forsyning":          {"url": "https://frederikshavnforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Hjørring Vandselskab":             {"url": "https://hjoerringvand.dk/nyheder/", "gruppe": "Forsyninger"},
    "Thisted Vand":                     {"url": "https://thistedvand.dk/nyheder/", "gruppe": "Forsyninger"},
    "Morsø Forsyning":                  {"url": "https://morsoeforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Rebild Forsyning":                 {"url": "https://rebildforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Mariagerfjord Vand":               {"url": "https://mariagerfjordvand.dk/nyheder/", "gruppe": "Forsyninger"},
    "Vesthimmerlands Vand":             {"url": "https://vhvand.dk/nyheder/", "gruppe": "Forsyninger"},
    "Jammerbugt Forsyning":             {"url": "https://jammerbugtvand.dk/nyheder/", "gruppe": "Forsyninger"},

    # ── FORSYNINGER – Sydjylland ──
    "Esbjerg Forsyning":                {"url": "https://esbjergforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Vejle Spildevand":                 {"url": "https://www.vejlespildevand.dk/nyheder/", "gruppe": "Forsyninger"},
    "Kolding Spildevand":               {"url": "https://koldingspildevand.dk/nyheder/", "gruppe": "Forsyninger"},
    "Fredericia Forsyning":             {"url": "https://fredericiaforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Haderslev Forsyning":              {"url": "https://haderslevforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Aabenraa Forsyning":               {"url": "https://aabenraaforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Sønderborg Forsyning":             {"url": "https://sonderborgforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Tønder Forsyning":                 {"url": "https://toenderforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Varde Forsyning":                  {"url": "https://vardeforsyning.dk/nyheder/", "gruppe": "Forsyninger"},

    # ── FORSYNINGER – Fyn ──
    "VandCenter Syd":                   {"url": "https://vandcenter.dk/nyheder/", "gruppe": "Forsyninger"},
    "Odense Renovation":                {"url": "https://www.odenserenovation.dk/nyheder/", "gruppe": "Forsyninger"},
    "Assens Forsyning":                 {"url": "https://assensforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Middelfart Spildevand":            {"url": "https://middelfartspildevand.dk/nyheder/", "gruppe": "Forsyninger"},
    "Faaborg-Midtfyn Fors.":            {"url": "https://fmfors.dk/nyheder/", "gruppe": "Forsyninger"},
    "Svendborg Spildevand":             {"url": "https://svendborgspildevand.dk/nyheder/", "gruppe": "Forsyninger"},
    "Nyborg Forsyning":                 {"url": "https://nyborgforsyning.dk/nyheder/", "gruppe": "Forsyninger"},

    # ── FORSYNINGER – Sjælland ──
    "Danva":                            {"url": "https://www.danva.dk/nyheder/", "gruppe": "Forsyninger"},
    "Kalundborg Forsyning":             {"url": "https://kalundborgforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Odsherred Forsyning":              {"url": "https://odsherredforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Holbæk Forsyning":                 {"url": "https://holbaekforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Slagelse Forsyning":               {"url": "https://slagelse-forsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Næstved Forsyning":                {"url": "https://naestvedforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Vordingborg Forsyning":            {"url": "https://vordingborgforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Guldborgsund Forsyning":           {"url": "https://guldborgsundforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Lolland Forsyning":                {"url": "https://lollandforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Ringsted Forsyning":               {"url": "https://ringstedforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Faxe Forsyning":                   {"url": "https://faxeforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Stevns Forsyning":                 {"url": "https://stevnsforsyning.dk/nyheder/", "gruppe": "Forsyninger"},
    "Bornholms Forsyning":              {"url": "https://bornholmsforsyning.dk/nyheder/", "gruppe": "Forsyninger"},

    # ── KOMMUNER – alle 98 ──
    "Kbh. Kommune":                     {"url": "https://www.kk.dk/nyheder", "gruppe": "Kommuner"},
    "Aarhus Kommune":                   {"url": "https://www.aarhus.dk/nyheder/", "gruppe": "Kommuner"},
    "Odense Kommune":                   {"url": "https://www.odense.dk/nyheder", "gruppe": "Kommuner"},
    "Aalborg Kommune":                  {"url": "https://www.aalborg.dk/nyheder", "gruppe": "Kommuner"},
    "Frederiksberg":                    {"url": "https://www.frederiksberg.dk/nyheder", "gruppe": "Kommuner"},
    "Vejle Kommune":                    {"url": "https://www.vejle.dk/nyheder", "gruppe": "Kommuner"},
    "Roskilde Kommune":                 {"url": "https://roskilde.dk/nyheder", "gruppe": "Kommuner"},
    "Helsingør Kommune":                {"url": "https://www.helsingor.dk/nyheder", "gruppe": "Kommuner"},
    "Næstved Kommune":                  {"url": "https://www.naestved.dk/nyheder", "gruppe": "Kommuner"},
    "Holstebro Kommune":                {"url": "https://www.holstebro.dk/nyheder", "gruppe": "Kommuner"},
    "Herning Kommune":                  {"url": "https://www.herning.dk/nyheder", "gruppe": "Kommuner"},
    "Silkeborg Kommune":                {"url": "https://www.silkeborg.dk/nyheder", "gruppe": "Kommuner"},
    "Horsens Kommune":                  {"url": "https://www.horsens.dk/nyheder", "gruppe": "Kommuner"},
    "Randers Kommune":                  {"url": "https://www.randers.dk/nyheder", "gruppe": "Kommuner"},
    "Kolding Kommune":                  {"url": "https://www.kolding.dk/nyheder", "gruppe": "Kommuner"},
    "Esbjerg Kommune":                  {"url": "https://www.esbjerg.dk/nyheder", "gruppe": "Kommuner"},
    "Sønderborg Kommune":               {"url": "https://www.sonderborg.dk/nyheder", "gruppe": "Kommuner"},
    "Fredericia Kommune":               {"url": "https://www.fredericia.dk/nyheder", "gruppe": "Kommuner"},
    "Viborg Kommune":                   {"url": "https://viborg.dk/nyheder", "gruppe": "Kommuner"},
    "Køge Kommune":                     {"url": "https://www.koege.dk/nyheder", "gruppe": "Kommuner"},
    "Slagelse Kommune":                 {"url": "https://www.slagelse.dk/nyheder", "gruppe": "Kommuner"},
    "Hillerød Kommune":                 {"url": "https://www.hillerod.dk/nyheder", "gruppe": "Kommuner"},
    "Faxe Kommune":                     {"url": "https://www.faxekommune.dk/nyheder", "gruppe": "Kommuner"},
    "Guldborgsund Kommune":             {"url": "https://www.guldborgsund.dk/nyheder", "gruppe": "Kommuner"},
    "Lolland Kommune":                  {"url": "https://www.lolland.dk/nyheder", "gruppe": "Kommuner"},
    "Vordingborg Kommune":              {"url": "https://www.vordingborg.dk/nyheder", "gruppe": "Kommuner"},
    "Ringkøbing-Skjern Kommune":        {"url": "https://www.rksk.dk/nyheder", "gruppe": "Kommuner"},
    "Ikast-Brande Kommune":             {"url": "https://www.ikast-brande.dk/nyheder", "gruppe": "Kommuner"},
    "Syddjurs Kommune":                 {"url": "https://syddjurs.dk/nyheder", "gruppe": "Kommuner"},
    "Norddjurs Kommune":                {"url": "https://www.norddjurs.dk/nyheder", "gruppe": "Kommuner"},
    "Favrskov Kommune":                 {"url": "https://www.favrskov.dk/nyheder", "gruppe": "Kommuner"},
    "Skanderborg Kommune":              {"url": "https://www.skanderborg.dk/nyheder", "gruppe": "Kommuner"},
    "Odder Kommune":                    {"url": "https://odder.dk/nyheder", "gruppe": "Kommuner"},
    "Hedensted Kommune":                {"url": "https://www.hedensted.dk/nyheder", "gruppe": "Kommuner"},
    "Frederikshavn Kommune":            {"url": "https://www.frederikshavn.dk/nyheder", "gruppe": "Kommuner"},
    "Hjørring Kommune":                 {"url": "https://www.hjoerring.dk/nyheder", "gruppe": "Kommuner"},
    "Thisted Kommune":                  {"url": "https://www.thisted.dk/nyheder", "gruppe": "Kommuner"},
    "Morsø Kommune":                    {"url": "https://www.morsoe.dk/nyheder", "gruppe": "Kommuner"},
    "Lemvig Kommune":                   {"url": "https://www.lemvig.dk/nyheder", "gruppe": "Kommuner"},
    "Struer Kommune":                   {"url": "https://struer.dk/nyheder", "gruppe": "Kommuner"},
    "Vesthimmerlands Kommune":          {"url": "https://www.vesthimmerland.dk/nyheder", "gruppe": "Kommuner"},
    "Rebild Kommune":                   {"url": "https://www.rebild.dk/nyheder", "gruppe": "Kommuner"},
    "Mariagerfjord Kommune":            {"url": "https://www.mariagerfjord.dk/nyheder", "gruppe": "Kommuner"},
    "Jammerbugt Kommune":               {"url": "https://www.jammerbugt.dk/nyheder", "gruppe": "Kommuner"},
    "Brønderslev Kommune":              {"url": "https://www.bronderslev.dk/nyheder", "gruppe": "Kommuner"},
    "Varde Kommune":                    {"url": "https://www.varde.dk/nyheder", "gruppe": "Kommuner"},
    "Fanø Kommune":                     {"url": "https://www.fanoe.dk/nyheder", "gruppe": "Kommuner"},
    "Billund Kommune":                  {"url": "https://www.billund.dk/nyheder", "gruppe": "Kommuner"},
    "Vejen Kommune":                    {"url": "https://www.vejen.dk/nyheder", "gruppe": "Kommuner"},
    "Haderslev Kommune":                {"url": "https://www.haderslev.dk/nyheder", "gruppe": "Kommuner"},
    "Aabenraa Kommune":                 {"url": "https://aabenraa.dk/nyheder", "gruppe": "Kommuner"},
    "Tønder Kommune":                   {"url": "https://www.toender.dk/nyheder", "gruppe": "Kommuner"},
    "Nyborg Kommune":                   {"url": "https://www.nyborg.dk/nyheder", "gruppe": "Kommuner"},
    "Kerteminde Kommune":               {"url": "https://www.kerteminde.dk/nyheder", "gruppe": "Kommuner"},
    "Assens Kommune":                   {"url": "https://www.assens.dk/nyheder", "gruppe": "Kommuner"},
    "Middelfart Kommune":               {"url": "https://www.middelfart.dk/nyheder", "gruppe": "Kommuner"},
    "Nordfyns Kommune":                 {"url": "https://www.nordfynskommune.dk/nyheder", "gruppe": "Kommuner"},
    "Faaborg-Midtfyn Kommune":          {"url": "https://www.fmk.dk/nyheder", "gruppe": "Kommuner"},
    "Svendborg Kommune":                {"url": "https://svendborg.dk/nyheder", "gruppe": "Kommuner"},
    "Langeland Kommune":                {"url": "https://www.langelandkommune.dk/nyheder", "gruppe": "Kommuner"},
    "Ærø Kommune":                      {"url": "https://aeroe.dk/nyheder", "gruppe": "Kommuner"},
    "Kalundborg Kommune":               {"url": "https://www.kalundborg.dk/nyheder", "gruppe": "Kommuner"},
    "Odsherred Kommune":                {"url": "https://www.odsherred.dk/nyheder", "gruppe": "Kommuner"},
    "Holbæk Kommune":                   {"url": "https://www.holbaek.dk/nyheder", "gruppe": "Kommuner"},
    "Sorø Kommune":                     {"url": "https://www.soroe.dk/nyheder", "gruppe": "Kommuner"},
    "Ringsted Kommune":                 {"url": "https://www.ringsted.dk/nyheder", "gruppe": "Kommuner"},
    "Stevns Kommune":                   {"url": "https://www.stevns.dk/nyheder", "gruppe": "Kommuner"},
    "Solrød Kommune":                   {"url": "https://www.solrod.dk/nyheder", "gruppe": "Kommuner"},
    "Greve Kommune":                    {"url": "https://www.greve.dk/nyheder", "gruppe": "Kommuner"},
    "Rødovre Kommune":                  {"url": "https://www.rodovre.dk/nyheder", "gruppe": "Kommuner"},
    "Brøndby Kommune":                  {"url": "https://www.brondby.dk/nyheder", "gruppe": "Kommuner"},
    "Hvidovre Kommune":                 {"url": "https://www.hvidovre.dk/nyheder", "gruppe": "Kommuner"},
    "Albertslund Kommune":              {"url": "https://www.albertslund.dk/nyheder", "gruppe": "Kommuner"},
    "Glostrup Kommune":                 {"url": "https://www.glostrup.dk/nyheder", "gruppe": "Kommuner"},
    "Ishøj Kommune":                    {"url": "https://www.ishoj.dk/nyheder", "gruppe": "Kommuner"},
    "Vallensbæk Kommune":               {"url": "https://www.vallensbaek.dk/nyheder", "gruppe": "Kommuner"},
    "Høje-Taastrup Kommune":            {"url": "https://www.htk.dk/nyheder", "gruppe": "Kommuner"},
    "Ballerup Kommune":                 {"url": "https://www.ballerup.dk/nyheder", "gruppe": "Kommuner"},
    "Gladsaxe Kommune":                 {"url": "https://www.gladsaxe.dk/nyheder", "gruppe": "Kommuner"},
    "Herlev Kommune":                   {"url": "https://www.herlev.dk/nyheder", "gruppe": "Kommuner"},
    "Gentofte Kommune":                 {"url": "https://www.gentofte.dk/nyheder", "gruppe": "Kommuner"},
    "Lyngby-Taarbæk Kommune":           {"url": "https://www.ltk.dk/nyheder", "gruppe": "Kommuner"},
    "Rudersdal Kommune":                {"url": "https://www.rudersdal.dk/nyheder", "gruppe": "Kommuner"},
    "Furesø Kommune":                   {"url": "https://furesoe.dk/nyheder", "gruppe": "Kommuner"},
    "Egedal Kommune":                   {"url": "https://www.egedal.dk/nyheder", "gruppe": "Kommuner"},
    "Hørsholm Kommune":                 {"url": "https://www.horsholm.dk/nyheder", "gruppe": "Kommuner"},
    "Fredensborg Kommune":              {"url": "https://www.fredensborg.dk/nyheder", "gruppe": "Kommuner"},
    "Gribskov Kommune":                 {"url": "https://www.gribskov.dk/nyheder", "gruppe": "Kommuner"},
    "Halsnæs Kommune":                  {"url": "https://www.halsnaes.dk/nyheder", "gruppe": "Kommuner"},
    "Frederikssund Kommune":            {"url": "https://www.frederikssund.dk/nyheder", "gruppe": "Kommuner"},
    "Lejre Kommune":                    {"url": "https://www.lejre.dk/nyheder", "gruppe": "Kommuner"},
    "Bornholm Kommune":                 {"url": "https://www.brk.dk/nyheder", "gruppe": "Kommuner"},
    "Christiansø":                      {"url": "https://www.christiansoe.dk/nyheder", "gruppe": "Kommuner"},
}
