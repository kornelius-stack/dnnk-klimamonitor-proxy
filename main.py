from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx
import xml.etree.ElementTree as ET
from datetime import datetime
import asyncio
import re

app = FastAPI(title="DNNK Klimamonitor Proxy")

# ── RSS-feeds for alle nyhedskilder ──
RSS_FEEDS = {
    "Ingeniøren":       "https://ing.dk/rss/alle",
    "Altinget":         "https://www.altinget.dk/miljoe/rss.aspx",
    "Teknik & Miljø":   "https://www.tm.dk/rss",
    "DR Nyheder":       "https://www.dr.dk/nyheder/service/feeds/allenyheder",
    "TV2 Nyheder":      "https://feeds.tv2.dk/nyheder/rss",
    "Politiken":        "https://politiken.dk/rss/senestenyt.rss",
    "Berlingske":       "https://www.berlingske.dk/rss/nyheder/nyheder.rss",
    "Miljøstyrelsen":   "https://mst.dk/service/nyheder/rss",
    "Klimatilpasning":  "https://klimatilpasning.dk/feed/",
    "DANVA":            "https://www.danva.dk/nyheder/rss",
}

# ── Klimatilpasnings-nøgleord for filtrering ──
KEYWORDS = [
    "klimatilpasning", "skybrud", "oversvømmelse", "regnvand", "LAR",
    "spildevand", "kloak", "kloakseparering", "vandforsyning", "vandværk",
    "kystbeskyttelse", "stormflod", "havvandsstigning", "klimasikring",
    "regnvandsbassin", "forsinkelse af regnvand", "grøn infrastruktur",
    "permeable belægning", "faskine", "regnbed", "blue-green", "SUDS",
    "EU vandrammedirektiv", "klimahandlingsplan", "DK2020",
    "Miljøstyrelsen", "klimatilpasningsplan", "separatkloakering",
    "renseanlæg", "pumpestation", "vandmiljø",
    # Nordiske termer (SE/NO/FI)
    "klimatanpassning", "översvämning", "dagvatten", "skyfallsplan",
    "klimaatilpasning", "overvannshåndtering", "flom", "stormflo",
    "tulvantorjunta", "hulevesi", "ilmastonmuutos",
    # EU projekter
    "Interreg", "LIFE programme", "Horizon Europe", "Climate-ADAPT",
    "nature-based solutions", "NbS", "climate resilience", "urban flooding",
    "water resilience", "flood risk", "coastal adaptation", "Copernicus",
    "Baltic Sea Region", "North Sea Region", "climate mission",
    # Forsikring & finans
    "skadedata", "klimarisiko", "oversvømmelseskortlægning", "stormflodsforsikring",
    "klimaskade", "forsikringsskade", "Realdania", "byfornyelse",
    # Teknologi & leverandører  
    "DHI", "MIKE URBAN", "SCALGO", "hydraulisk model", "regnvandsmodel",
    "pumpestation", "separatkloakering", "Grundfos", "Wavin",
    # Regulering & jura
    "Stormrådet", "kystbeskyttelsesloven", "planloven", "oversvømmelsesdirektiv",
    "klimatilpasningsloven", "vandrammedirektiv", "høringsforslag",
    "bekendtgørelse", "Forsyningstilsynet",
    # Internationale
    "C40", "ICLEI", "Deltares", "IWA", "water resilience",
    "sponge city", "blue-green infrastructure", "urban water"
]

# Tillad kald fra alle origins (din dashboard HTML-fil)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# ── TED EU API ──
@app.get("/ted")
async def search_ted(q: str = Query("klimatilpasning"), size: int = 10):
    url = "https://api.ted.europa.eu/v3/notices/search"
    params = {
        "q": f"{q} Denmark",
        "pageSize": size,
        "fields": "title,organisations,publicationDate,contractValue,cpvCodes,noticeType,tedPublicationUrl",
        "country": "DNK"
    }
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(url, params=params)
        return resp.json()

# ── CVR API ──
@app.get("/cvr")
async def search_cvr(q: str = Query("vandforsyning")):
    url = "https://cvrapi.dk/api"
    params = {"search": q, "country": "dk", "limit": 10}
    headers = {"User-Agent": "DNNK-KlimaMonitor/1.0"}
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(url, params=params, headers=headers)
        return resp.json()

# ── CVR branchekode-søgning (vand=360000, spildevand=370000) ──
@app.get("/cvr/forsyninger")
async def get_forsyninger(branche: str = Query("360000")):
    # Elasticsearch endpoint for Virk's open CVR data
    url = "https://raw.data.api.virk.dk/cvr-permanent/virksomhed/_search"
    body = {
        "query": {
            "bool": {
                "must": [
                    {"term": {"Vrvirksomhed.virksomhedMetadata.nyesteBranchekode.branchekode": branche}},
                    {"term": {"Vrvirksomhed.virksomhedMetadata.sammensatStatus": "NORMAL"}}
                ]
            }
        },
        "_source": ["Vrvirksomhed.virksomhedMetadata.nyesteNavn",
                    "Vrvirksomhed.cvrNummer",
                    "Vrvirksomhed.virksomhedMetadata.nyesteBeliggenhedsadresse"],
        "size": 50
    }
    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.post(url, json=body,
            headers={"Content-Type": "application/json"})
        return resp.json()

# ── Plandata WFS ──
@app.get("/plandata")
async def get_plandata(kommunekode: str = Query(None)):
    base = "https://api.dataforsyningen.dk/rest/gst/plandata/v2/spildevandsomraader"
    params = {"format": "json", "limit": 20}
    if kommunekode:
        params["kommunekode"] = kommunekode
    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.get(base, params=params)
        return resp.json()

# ── RSS hjælpefunktion: hent og parse ét feed ──
async def fetch_rss(client: httpx.AsyncClient, source: str, url: str, query: str) -> list:
    try:
        resp = await client.get(url, timeout=10, follow_redirects=True,
            headers={"User-Agent": "DNNK-KlimaMonitor/1.0 (rss-reader)"})
        if resp.status_code != 200:
            return []

        root_el = ET.fromstring(resp.text)
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        items = root_el.findall(".//item") or root_el.findall(".//atom:entry", ns)

        results = []
        q_lower = query.lower()
        kw_lower = [k.lower() for k in KEYWORDS]

        for item in items[:40]:  # Tjek max 40 artikler per feed
            def get(tag):
                el = item.find(tag) or item.find(f"atom:{tag}", ns)
                return (el.text or "").strip() if el is not None else ""

            title       = get("title")
            description = get("description") or get("summary")
            link        = get("link") or get("id")
            pub_date    = get("pubDate") or get("published") or get("updated")

            # Rens HTML fra description
            description = re.sub(r"<[^>]+>", "", description)[:400]

            # Kombiner tekst til relevanstjek
            combined = (title + " " + description).lower()

            # Tjek om artiklen matcher søgeord ELLER brugerens query
            kw_match = any(kw in combined for kw in kw_lower)
            q_match  = any(w in combined for w in q_lower.split() if len(w) > 3)

            if not (kw_match or q_match):
                continue

            # Relevance score: antal nøgleord der matcher
            score = sum(1 for kw in kw_lower if kw in combined)
            score += (3 if q_match else 0)

            results.append({
                "source":      "news",
                "feedSource":  source,
                "title":       title,
                "org":         source,
                "date":        pub_date[:10] if pub_date else "",
                "summary":     description,
                "tags":        [kw for kw in KEYWORDS[:6] if kw.lower() in combined][:3],
                "relevance":   min(round(score / 8, 2), 1.0),
                "url":         link,
                "value":       None
            })

        # Sortér efter relevans og returnér top 5 per kilde
        results.sort(key=lambda x: x["relevance"], reverse=True)
        return results[:5]

    except Exception:
        return []


# ── NEWS endpoint: henter fra alle RSS-feeds parallelt ──
@app.get("/news")
async def get_news(q: str = Query("klimatilpasning"), sources: str = Query(None)):
    # Vælg feeds – alle eller specifik liste
    feeds_to_use = RSS_FEEDS
    if sources:
        wanted = [s.strip() for s in sources.split(",")]
        feeds_to_use = {k: v for k, v in RSS_FEEDS.items() if k in wanted}

    async with httpx.AsyncClient() as client:
        tasks = [fetch_rss(client, src, url, q) for src, url in feeds_to_use.items()]
        results_nested = await asyncio.gather(*tasks)

    # Flat liste, sortér samlet efter relevans
    all_articles = [art for sublist in results_nested for art in sublist]
    all_articles.sort(key=lambda x: (x["relevance"], x["date"]), reverse=True)

    return {
        "articles":   all_articles,
        "total":      len(all_articles),
        "sources":    {src: len([a for a in all_articles if a["feedSource"] == src])
                       for src in feeds_to_use},
        "query":      q,
        "scanned_at": datetime.utcnow().isoformat()
    }


# ── Health check ──
@app.get("/")
def root():
    return {
        "status":    "ok",
        "service":   "DNNK Klimamonitor Proxy",
        "endpoints": ["/ted", "/cvr", "/cvr/forsyninger", "/plandata", "/news"]
    }


# ══════════════════════════════════════════════════════════════
# UDVIDET NEWS-ENDPOINT med alle DNNK-relevante kilder
# ══════════════════════════════════════════════════════════════
from sources import ALL_FEEDS_FLAT, ALLE_FEEDS

@app.get("/news/full")
async def get_news_full(
    q: str = Query("klimatilpasning"),
    gruppe: str = Query(None),   # fx "Rådgivere" eller "Vidensinstitutioner"
    limit: int = Query(5)        # max resultater per kilde
):
    """Henter fra alle 60+ DNNK-relevante RSS-feeds parallelt"""
    feeds = ALL_FEEDS_FLAT
    if gruppe and gruppe in ALLE_FEEDS:
        feeds = {k: {"url": v, "gruppe": gruppe}
                 for k, v in ALLE_FEEDS[gruppe].items()}

    async with httpx.AsyncClient() as client:
        tasks = [
            fetch_rss(client, navn, meta["url"], q)
            for navn, meta in feeds.items()
        ]
        nested = await asyncio.gather(*tasks)

    all_articles = []
    for i, (navn, meta) in enumerate(feeds.items()):
        for art in nested[i][:limit]:
            art["gruppe"] = meta["gruppe"]
            all_articles.append(art)

    all_articles.sort(key=lambda x: (x["relevance"], x["date"]), reverse=True)

    return {
        "articles":   all_articles,
        "total":      len(all_articles),
        "feeds_checked": len(feeds),
        "per_gruppe": {
            g: len([a for a in all_articles if a.get("gruppe") == g])
            for g in ALLE_FEEDS
        },
        "query":      q,
        "scanned_at": datetime.utcnow().isoformat()
    }


@app.get("/news/kilder")
async def get_kilder():
    """Returnerer komplet liste over alle overvågede kilder"""
    return {
        gruppe: list(feeds.keys())
        for gruppe, feeds in ALLE_FEEDS.items()
    }
