import asyncio
import httpx
import os
from datetime import datetime, timezone, timedelta

BREVO_API_KEY = os.environ.get("BREVO_API_KEY", "")
DIGEST_EMAIL_TO = os.environ.get("DIGEST_EMAIL_TO", "kp@dnnk.dk")
DIGEST_EMAIL_FROM = os.environ.get("DIGEST_EMAIL_FROM", "kp@dnnk.dk")
DIGEST_EMAIL_FROM_NAME = "DNNK Klimamonitor"

QUERIES = [
    "klimatilpasning skybrud",
    "LAR regnvand",
    "vandforsyning renovering",
    "spildevand klimasikring",
    "kystbeskyttelse oversvømmelse",
]

async def fetch_articles(query: str, limit: int = 3) -> list:
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(
                "http://localhost:10000/news/full",
                params={"q": query, "limit": limit}
            )
            data = resp.json()
            return data.get("articles", [])
    except Exception as e:
        print(f"Fejl ved hentning af artikler for '{query}': {e}")
        return []

async def fetch_ted(query: str, size: int = 5) -> list:
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(
                "http://localhost:10000/ted",
                params={"q": query, "size": size}
            )
            data = resp.json()
            return data.get("notices", data.get("results", []))
    except Exception as e:
        print(f"Fejl ved hentning af TED-udbud: {e}")
        return []

def build_html_email(articles: list, ted_notices: list, scan_date: str) -> str:
    article_rows = ""
    seen = set()
    for art in articles:
        key = art.get("title", "")
        if key in seen:
            continue
        seen.add(key)
        tags = ", ".join(art.get("tags", []))
        url = art.get("url", "#")
        article_rows += f"""
        <tr>
          <td style="padding:10px 0; border-bottom:1px solid #e8f0e0;">
            <a href="{url}" style="color:#2d6a4f;font-weight:bold;text-decoration:none;">{art.get('title','')}</a><br>
            <span style="color:#666;font-size:12px;">{art.get('feedSource','')} · {art.get('date','')}</span><br>
            <span style="color:#444;font-size:13px;">{art.get('summary','')[:200]}...</span><br>
            <span style="color:#888;font-size:11px;">{tags}</span>
          </td>
        </tr>"""

    ted_rows = ""
    for notice in ted_notices[:5]:
        title = notice.get("title", {})
        if isinstance(title, dict):
            title = title.get("dan", title.get("eng", "Uden titel"))
        url = notice.get("tedPublicationUrl", "#")
        date = notice.get("publicationDate", "")[:10]
        ted_rows += f"""
        <tr>
          <td style="padding:10px 0; border-bottom:1px solid #e8f0e0;">
            <a href="{url}" style="color:#1a4d6e;font-weight:bold;text-decoration:none;">{title}</a><br>
            <span style="color:#666;font-size:12px;">TED EU · {date}</span>
          </td>
        </tr>"""

    if not ted_rows:
        ted_rows = "<tr><td style='color:#888;padding:10px 0;'>Ingen nye EU-udbud fundet i dag.</td></tr>"

    return f"""
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family:Arial,sans-serif;max-width:680px;margin:0 auto;background:#f9fdf6;padding:20px;">
  <div style="background:#2d6a4f;padding:24px;border-radius:8px 8px 0 0;">
    <h1 style="color:white;margin:0;font-size:22px;">🌿 DNNK Klimamonitor</h1>
    <p style="color:#b7e4c7;margin:6px 0 0;">Daglig scanning · {scan_date}</p>
  </div>
  <div style="background:white;padding:24px;border-radius:0 0 8px 8px;box-shadow:0 2px 8px rgba(0,0,0,0.08);">
    <h2 style="color:#2d6a4f;border-bottom:2px solid #b7e4c7;padding-bottom:8px;">📰 Nyheder og fagartikler</h2>
    <table width="100%" cellpadding="0" cellspacing="0">
      {article_rows if article_rows else "<tr><td style='color:#888;padding:10px 0;'>Ingen relevante nyheder fundet i dag.</td></tr>"}
    </table>
    <h2 style="color:#1a4d6e;border-bottom:2px solid #bee3f8;padding-bottom:8px;margin-top:32px;">🇪🇺 EU-udbud (TED)</h2>
    <table width="100%" cellpadding="0" cellspacing="0">
      {ted_rows}
    </table>
    <p style="color:#aaa;font-size:11px;margin-top:32px;border-top:1px solid #eee;padding-top:12px;">
      Sendt automatisk af DNNK Klimamonitor · 153 RSS-feeds · 
      <a href="https://dnnk-klimamonitor-proxy.onrender.com" style="color:#aaa;">dnnk-klimamonitor-proxy.onrender.com</a>
    </p>
  </div>
</body>
</html>"""

async def send_brevo_email(subject: str, html_content: str):
    if not BREVO_API_KEY:
        print("ADVARSEL: BREVO_API_KEY ikke sat – e-mail ikke sendt")
        return

    payload = {
        "sender": {"name": DIGEST_EMAIL_FROM_NAME, "email": DIGEST_EMAIL_FROM},
        "to": [{"email": DIGEST_EMAIL_TO}],
        "subject": subject,
        "htmlContent": html_content
    }

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            "https://api.brevo.com/v3/smtp/email",
            json=payload,
            headers={
                "api-key": BREVO_API_KEY,
                "Content-Type": "application/json"
            }
        )
        if resp.status_code in (200, 201):
            print(f"E-mail sendt til {DIGEST_EMAIL_TO} via Brevo ✅")
        else:
            print(f"Brevo fejl {resp.status_code}: {resp.text}")

async def run_daily_digest():
    print(f"[{datetime.now().strftime('%H:%M')}] Starter daglig scanning...")

    all_articles = []
    for query in QUERIES:
        articles = await fetch_articles(query, limit=3)
        all_articles.extend(articles)

    ted_notices = await fetch_ted("klimatilpasning skybrud", size=5)

    # Dedupliker
    seen = set()
    unique_articles = []
    for art in all_articles:
        key = art.get("title", "")
        if key not in seen:
            seen.add(key)
            unique_articles.append(art)

    unique_articles.sort(key=lambda x: (x.get("relevance", 0), x.get("date", "")), reverse=True)

    scan_date = datetime.now().strftime("%d. %B %Y")
    html = build_html_email(unique_articles[:20], ted_notices, scan_date)
    subject = f"DNNK Klimamonitor · {scan_date} · {len(unique_articles)} nyheder"

    print(f"Fundet {len(unique_articles)} nyheder og {len(ted_notices)} TED-udbud")
    await send_brevo_email(subject, html)

async def scheduler_loop():
    cph = timezone(timedelta(hours=1))
    print("Scheduler startet – venter på kl. 08:00...")
    while True:
        now = datetime.now(cph)
        next_run = now.replace(hour=8, minute=0, second=0, microsecond=0)
        if now >= next_run:
            next_run = next_run + timedelta(days=1)
        wait_seconds = (next_run - now).total_seconds()
        print(f"Næste scanning: {next_run.strftime('%d/%m %H:%M')} (om {int(wait_seconds // 3600)}t {int((wait_seconds % 3600) // 60)}m)")
        await asyncio.sleep(wait_seconds)
        await run_daily_digest()
