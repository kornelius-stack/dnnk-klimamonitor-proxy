from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx
import xml.etree.ElementTree as ET
from datetime import datetime
import asyncio
import re

app = FastAPI(title="DNNK Klimamonitor Proxy")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

KEYWORDS = [
    "klimatilpasning", "skybrud", "oversvømmelse", "regnvand", "LAR",
    "spildevand", "kloak", "kloakseparering", "vandforsyning", "vandværk",
    "kystbeskyttelse", "stormflod", "havvandsstigning", "klimasikring",
    "regnvandsbassin", "grøn infrastruktur", "permeable belægning",
    "faskine", "regnbed", "klimahandlingsplan", "DK2020",
    "separatkloakering", "renseanlæg", "pumpestation", "vandmiljø",
    "klimatanpassning", "översvämning", "dagvatten", "overvannshåndtering",
    "Interreg", "LIFE programme", "Horizon Europe", "Climate-ADAPT",
    "nature-based solutions", "flood risk", "coastal adaptation",
    "DHI", "SCALGO", "Stormrådet", "Realdania", "klimarisiko",
    "C40", "ICLEI", "Deltares", "water resilience",
    "klima", "vand", "miljø", "natur", "bæredygtig",
    "climate", "water", "flood", "urban", "infrastructure"
]

def parse_item(item):
    title = ""
    description = ""
    link = ""
    pub_date = ""
    for child in item:
        tag = child.tag.split("}")[-1] if "}" in child.tag else child.tag
        text = (child.text or "").strip()
        if tag == "title" and not title:
            title = text
        elif tag in ("description", "summary", "content") and not description:
            description = re.sub(r"<[^>]+>", "", text)[:400]
        elif tag == "link" and not link:
            href = child.get("href", "")
            link = href if href else text
        elif tag == "id" and not link:
            link = text
        elif tag in ("pubDate", "published", "updated", "date") and not pub_date:
            pub_date = text[:10] if text else ""
    return title, description, link, pub_date

async def fetch_rss(client, source, url, query):
    try:
        resp = await client.get(url, timeout=15, follow_redirects=True,
            headers={"User-Agent": "DNNK-KlimaMonitor/1.0"})
        if resp.status_code != 200:
            return []
        content = re.sub(r' xmlns[^=]*="[^"]*"', '', resp.text)
        content = re.sub(r'<\?xml[^>]*\?>', '', content)
        try:
            root_el = ET.fromstring(content)
        except ET.ParseError:
            return []
        items = root_el.findall(".//item") + root_el.findall(".//entry")
        if not items:
            return []
        results = []
        q_lower = query.lower()
        kw_lower = [k.lower() for k in KEYWORDS]
        for item in items[:20]:
            title, description, link, pub_date = parse_item(item)
            if not title:
                continue
            combined = (title + " " + description).lower()
            q_match = any(w in combined for w in q_lower.split() if len(w) > 3)
            score = sum(1 for kw in kw_lower if kw in combined) + (3 if q_match else 0)
            results.append({
                "source": "news", "feedSource": source, "title": title,
                "org": source, "date": pub_date, "summary": description,
                "tags": [kw for kw in KEYWORDS[:6] if kw.lower() in combined][:3],
                "relevance": min(round(score / 8, 2), 1.0), "url": link, "value": None
            })
        results.sort(key=lambda x: x["relevance"], reverse=True)
        return results[:5]
    except Exception:
        return []

@app.get("/ted")
async def search_ted(q: str = Query("klimatilpasning"), size: int = 10):
    url = "https://api.ted.europa.eu/v3/notices/search"
    params = {"q": f"{q} Denmark", "pageSize": size,
              "fields": "title,organisations,publicationDate,contractValue,cpvCodes,noticeType,tedPublicationUrl",
              "country": "DNK"}
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(url, params=params)
        return resp.json()

@app.get("/cvr")
async def search_cvr(q: str = Query("vandforsyning")):
    url = "https://cvrapi.dk/api"
    params = {"search": q, "country": "dk", "limit": 10}
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(url, params=params,
            headers={"User-Agent": "DNNK-KlimaMonitor/1.0"})
        return resp.json()

@app.get("/cvr/forsyninger")
async def get_forsyninger(branche: str = Query("360000")):
    url = "https://raw.data.api.virk.dk/cvr-permanent/virksomhed/_search"
    body = {"query": {"bool": {"must": [
        {"term": {"Vrvirksomhed.virksomhedMetadata.nyesteBranchekode.branchekode": branche}},
        {"term": {"Vrvirksomhed.virksomhedMetadata.sammensatStatus": "NORMAL"}}
    ]}}, "size": 50}
    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.post(url, json=body)
        return resp.json()

@app.get("/plandata")
async def get_plandata(kommunekode: str = Query(None)):
    base = "https://api.dataforsyningen.dk/rest/gst/plandata/v2/spildevandsomraader"
    params = {"format": "json", "limit": 20}
    if kommunekode:
        params["kommunekode"] = kommunekode
    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.get(base, params=params)
        return resp.json()

@app.get("/news")
async def get_news(q: str = Query("klimatilpasning")):
    from sources import RSS_NEWS
    async with httpx.AsyncClient() as client:
        tasks = [fetch_rss(client, src, url, q) for src, url in RSS_NEWS.items()]
        nested = await asyncio.gather(*tasks)
    articles = [a for sub in nested for a in sub]
    articles.sort(key=lambda x: (x["relevance"], x["date"]), reverse=True)
    return {"articles": articles, "total": len(articles), "query": q}

@app.get("/news/full")
async def get_news_full(q: str = Query("klimatilpasning"), gruppe: str = Query(None), limit: int = Query(5)):
    from sources import ALL_FEEDS_FLAT, ALLE_FEEDS
    feeds = ALL_FEEDS_FLAT
    if gruppe and gruppe in ALLE_FEEDS:
        feeds = {k: {"url": v, "gruppe": gruppe} for k, v in ALLE_FEEDS[gruppe].items()}
    async with httpx.AsyncClient() as client:
        tasks = [fetch_rss(client, navn, meta["url"], q) for navn, meta in feeds.items()]
        nested = await asyncio.gather(*tasks)
    articles = []
    for i, (navn, meta) in enumerate(feeds.items()):
        for art in nested[i][:limit]:
            art["gruppe"] = meta["gruppe"]
            articles.append(art)
    articles.sort(key=lambda x: (x["relevance"], x["date"]), reverse=True)
    return {"articles": articles, "total": len(articles),
            "feeds_checked": len(feeds), "query": q,
            "scanned_at": datetime.utcnow().isoformat()}

@app.get("/news/kilder")
async def get_kilder():
    from sources import ALLE_FEEDS
    return {gruppe: list(feeds.keys()) for gruppe, feeds in ALLE_FEEDS.items()}

@app.get("/send-digest")
async def trigger_digest():
    asyncio.create_task(_run_digest())
    return {"status": "Digest scanning startet – e-mail sendes om ca. 60 sek"}

async def _run_digest():
    try:
        from scheduler import run_daily_digest
        await run_daily_digest()
    except Exception as e:
        print(f"Digest fejl: {e}")

@app.on_event("startup")
async def start_scheduler():
    asyncio.create_task(_scheduler_loop())

async def _scheduler_loop():
    try:
        from scheduler import scheduler_loop
        await scheduler_loop()
    except Exception as e:
        print(f"Scheduler fejl: {e}")

@app.get("/")
def root():
    return {"status": "ok", "service": "DNNK Klimamonitor Proxy",
            "endpoints": ["/ted", "/cvr", "/plandata", "/news", "/news/full", "/send-digest"]}
