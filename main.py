from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
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

RSS_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/rss+xml, application/xml, text/xml, */*",
    "Accept-Language": "da,en;q=0.9",
}

def parse_item_bs(item):
    """Parse et RSS/Atom item med BeautifulSoup"""
    title = item.find("title")
    title = title.get_text(strip=True) if title else ""
    
    desc = item.find("description") or item.find("summary") or item.find("content")
    description = re.sub(r"<[^>]+>", "", desc.get_text(strip=True))[:400] if desc else ""
    
    link = item.find("link")
    if link:
        url = link.get("href") or link.get_text(strip=True)
    else:
        url = ""
    
    for tag in ["pubdate", "published", "updated", "date"]:
        d = item.find(tag)
        if d:
            pub_date = d.get_text(strip=True)[:10]
            break
    else:
        pub_date = ""
    
    return title, description, url, pub_date

def parse_item_et(item):
    """Parse et RSS/Atom item med ElementTree"""
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
        resp = await client.get(url, timeout=15, follow_redirects=True, headers=RSS_HEADERS)
        if resp.status_code != 200:
            return []
        
        content = resp.text
        items = []
        
        # Prøv først ElementTree
        try:
            clean = re.sub(r' xmlns[^=]*="[^"]*"', '', content)
            clean = re.sub(r'<\?xml[^>]*\?>', '', clean)
            root_el = ET.fromstring(clean)
            et_items = root_el.findall(".//item") + root_el.findall(".//entry")
            if et_items:
                items = [("et", i) for i in et_items]
        except ET.ParseError:
            pass
        
        # Fallback: BeautifulSoup
        if not items:
            try:
                soup = BeautifulSoup(content, "xml")
                bs_items = soup.find_all("item") + soup.find_all("entry")
                if bs_items:
                    items = [("bs", i) for i in bs_items]
            except Exception:
                try:
                    soup = BeautifulSoup(content, "lxml")
                    bs_items = soup.find_all("item") + soup.find_all("entry")
                    if bs_items:
                        items = [("bs", i) for i in bs_items]
                except Exception:
                    pass
        
        if not items:
            return []
        
        results = []
        q_lower = query.lower()
        kw_lower = [k.lower() for k in KEYWORDS]
        
        for parser, item in items[:20]:
            if parser == "et":
                title, description, link, pub_date = parse_item_et(item)
            else:
                title, description, link, pub_date = parse_item_bs(item)
            
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

@app.get("/test-feeds")
async def test_feeds():
    """Test alle RSS feeds og returner status for hver"""
    from sources import ALL_FEEDS_FLAT

    async def check_feed(navn, meta):
        url = meta["url"]
        gruppe = meta["gruppe"]
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(url, follow_redirects=True, headers=RSS_HEADERS)
                if resp.status_code != 200:
                    return {"navn": navn, "gruppe": gruppe, "url": url,
                            "status": "fejl", "info": f"HTTP {resp.status_code}"}
                content = resp.text
                # Prøv ET
                try:
                    clean = re.sub(r' xmlns[^=]*="[^"]*"', '', content)
                    root = ET.fromstring(clean)
                    items = root.findall(".//item") + root.findall(".//entry")
                    if items:
                        return {"navn": navn, "gruppe": gruppe, "url": url,
                                "status": "ok", "info": f"{len(items)} items (ET)"}
                except ET.ParseError:
                    pass
                # Prøv BS
                try:
                    soup = BeautifulSoup(content, "xml")
                    items = soup.find_all("item") + soup.find_all("entry")
                    if items:
                        return {"navn": navn, "gruppe": gruppe, "url": url,
                                "status": "ok", "info": f"{len(items)} items (BS)"}
                except Exception:
                    pass
                return {"navn": navn, "gruppe": gruppe, "url": url,
                        "status": "fejl", "info": "Ingen items fundet"}
        except Exception as e:
            return {"navn": navn, "gruppe": gruppe, "url": url,
                    "status": "fejl", "info": str(e)[:80]}

    tasks = [check_feed(n, m) for n, m in ALL_FEEDS_FLAT.items()]
    results = await asyncio.gather(*tasks)
    ok = [r for r in results if r["status"] == "ok"]
    fejl = [r for r in results if r["status"] != "ok"]
    return {
        "total": len(results), "ok": len(ok), "fejl": len(fejl),
        "virker": sorted(ok, key=lambda x: x["gruppe"]),
        "virker_ikke": sorted(fejl, key=lambda x: x["gruppe"]),
        "testet": datetime.utcnow().isoformat()
    }

@app.get("/ted")
async def search_ted(q: str = Query("klimatilpasning"), size: int = 10):
    url = "https://api.ted.europa.eu/v3/notices/search"
    params = {"q": f"{q} Denmark", "pageSize": size,
              "fields": "title,organisations,publicationDate,contractValue,cpvCodes,noticeType,tedPublicationUrl",
              "country": "DNK"}
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(url, params=params)
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
            "endpoints": ["/ted", "/news", "/news/full", "/news/kilder", "/test-feeds"]}


# ─────────────────────────────────────────────────────────────
# SCRAPING — til sider uden RSS
# ─────────────────────────────────────────────────────────────

# SCRAPE_SOURCES importeres fra sources.py
from sources import SCRAPE_SOURCES

async def scrape_news(client, source, url, gruppe, query):
    """Scraper nyhedsartikler direkte fra hjemmeside HTML"""
    try:
        resp = await client.get(url, timeout=15, follow_redirects=True, headers=RSS_HEADERS)
        if resp.status_code != 200:
            return []

        soup = BeautifulSoup(resp.text, "lxml")

        # Fjern navigation, footer, scripts
        for tag in soup(["nav", "footer", "script", "style", "header"]):
            tag.decompose()

        articles = []
        q_lower = query.lower()
        kw_lower = [k.lower() for k in KEYWORDS]

        # Find artikelementer — prøv mange mønstre
        candidates = (
            soup.find_all("article") or
            soup.find_all(class_=re.compile(r"news|nyhed|artikel|post|teaser|card", re.I)) or
            soup.find_all("li", class_=re.compile(r"news|nyhed|artikel|post|item", re.I))
        )

        if not candidates:
            # Fallback: find alle h2/h3 links
            candidates = soup.find_all(["h2", "h3"])

        seen_titles = set()
        for el in candidates[:20]:
            # Find titel
            title_el = (
                el.find(["h1", "h2", "h3", "h4"]) or
                el if el.name in ["h2", "h3"] else None
            )
            if not title_el:
                continue
            title = title_el.get_text(strip=True)
            if not title or len(title) < 10 or title in seen_titles:
                continue
            seen_titles.add(title)

            # Find link
            link_el = title_el.find("a") or el.find("a")
            article_url = ""
            if link_el and link_el.get("href"):
                href = link_el["href"]
                if href.startswith("http"):
                    article_url = href
                elif href.startswith("/"):
                    from urllib.parse import urlparse
                    base = urlparse(url)
                    article_url = f"{base.scheme}://{base.netloc}{href}"

            # Find dato
            date_el = el.find(["time"]) or el.find(class_=re.compile(r"date|dato|tid", re.I))
            pub_date = ""
            if date_el:
                pub_date = (date_el.get("datetime") or date_el.get_text(strip=True))[:10]

            # Find beskrivelse
            desc_el = el.find("p")
            description = desc_el.get_text(strip=True)[:300] if desc_el else ""

            combined = (title + " " + description).lower()
            q_match = any(w in combined for w in q_lower.split() if len(w) > 3)
            score = sum(1 for kw in kw_lower if kw in combined) + (3 if q_match else 0)

            articles.append({
                "source": "scrape",
                "feedSource": source,
                "title": title,
                "org": source,
                "date": pub_date,
                "summary": description,
                "tags": [kw for kw in KEYWORDS[:6] if kw.lower() in combined][:3],
                "relevance": min(round(score / 8, 2), 1.0),
                "url": article_url,
                "value": None,
                "gruppe": gruppe,
            })

        articles.sort(key=lambda x: x["relevance"], reverse=True)
        return articles[:5]

    except Exception:
        return []


@app.get("/news/scrape")
async def get_scraped_news(q: str = Query("klimatilpasning")):
    """Hent nyheder via direkte scraping fra sider uden RSS"""
    async with httpx.AsyncClient() as client:
        tasks = [
            scrape_news(client, navn, meta["url"], meta["gruppe"], q)
            for navn, meta in SCRAPE_SOURCES.items()
        ]
        nested = await asyncio.gather(*tasks)

    articles = [a for sub in nested for a in sub]
    articles.sort(key=lambda x: (x["relevance"], x["date"]), reverse=True)
    return {
        "articles": articles,
        "total": len(articles),
        "sources_checked": len(SCRAPE_SOURCES),
        "query": q,
        "scanned_at": datetime.utcnow().isoformat()
    }
