# ─────────────────────────────────────────────────────────────
# DNNK Klimamonitor – Daglig e-mail digest kl. 8:00
# Kræver miljøvariable på Render:
#   SENDGRID_API_KEY  ← din SendGrid API-nøgle
#   DIGEST_EMAIL_TO   ← fx info@dnnk.dk
#   DIGEST_EMAIL_FROM ← fx klimamonitor@dnnk.dk
# ─────────────────────────────────────────────────────────────

import asyncio
import os
import httpx
from datetime import datetime, timezone, timedelta
import json

# SendGrid
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")
EMAIL_TO         = os.getenv("DIGEST_EMAIL_TO", "info@dnnk.dk")
EMAIL_FROM       = os.getenv("DIGEST_EMAIL_FROM", "klimamonitor@dnnk.dk")
PROXY_BASE       = os.getenv("PROXY_URL", "https://dnnk-klimamonitor-proxy.onrender.com")

# Standard søgeord til daglig scanning
DEFAULT_QUERIES = [
    "klimatilpasning skybrud",
    "LAR regnvand",
    "kystbeskyttelse oversvømmelse",
    "spildevand klimasikring",
    "vandforsyning renovering"
]

async def fetch_news(query: str) -> list:
    """Hent nyheder fra proxyen"""
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(
                f"{PROXY_BASE}/news/full",
                params={"q": query, "limit": 3}
            )
            if resp.status_code == 200:
                data = resp.json()
                return data.get("articles", [])
    except Exception as e:
        print(f"Fejl ved hentning af nyheder for '{query}': {e}")
    return []

async def fetch_ted(query: str) -> list:
    """Hent TED-udbud fra proxyen"""
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(
                f"{PROXY_BASE}/ted",
                params={"q": query, "size": 5}
            )
            if resp.status_code == 200:
                data = resp.json()
                notices = data.get("notices", [])
                return [{
                    "title": (n.get("title") or [{}])[0].get("value", "Udbud"),
                    "org": (n.get("organisations") or [{}])[0].get("officialName", "—"),
                    "date": n.get("publicationDate", ""),
                    "url": n.get("tedPublicationUrl", "https://ted.europa.eu"),
                    "value": n.get("contractValue"),
                    "source": "TED EU"
                } for n in notices[:5]]
    except Exception as e:
        print(f"Fejl ved hentning af TED for '{query}': {e}")
    return []

def build_html_email(all_news: list, all_ted: list, dato: str) -> str:
    """Byg HTML e-mail"""

    # Grupper nyheder efter kilde-gruppe
    groups = {}
    for art in all_news:
        g = art.get("gruppe", art.get("feedSource", "Andre"))
        groups.setdefault(g, []).append(art)

    # Byg nyheds-sektioner
    news_html = ""
    for gruppe, artikler in sorted(groups.items()):
        # Kun top 3 per gruppe
        top = sorted(artikler, key=lambda x: x.get("relevance", 0), reverse=True)[:3]
        if not top:
            continue
        news_html += f"""
        <tr><td style="padding:20px 0 8px;">
            <div style="font-size:11px;letter-spacing:2px;text-transform:uppercase;
                        color:#6a8a6a;font-family:monospace;">{gruppe}</div>
        </td></tr>"""
        for a in top:
            relevance_pct = int(a.get("relevance", 0) * 100)
            tags = " · ".join(a.get("tags", [])[:3])
            news_html += f"""
        <tr><td style="padding:6px 0 14px;border-bottom:1px solid #e8e4d8;">
            <a href="{a.get('url','#')}" style="font-family:Georgia,serif;font-size:15px;
               font-weight:600;color:#1a3a1a;text-decoration:none;line-height:1.4;
               display:block;margin-bottom:4px;">{a.get('title','')}</a>
            <div style="font-size:11px;color:#6a7a6a;margin-bottom:6px;font-family:monospace;">
                {a.get('feedSource','')}{' · ' + a.get('date','')[:10] if a.get('date') else ''}
                {' · <span style="color:#2d7a2d;">▮ ' + str(relevance_pct) + '% relevant</span>' if relevance_pct > 50 else ''}
            </div>
            <div style="font-size:13px;color:#4a5a4a;line-height:1.6;">
                {a.get('summary','')[:200]}{'...' if len(a.get('summary','')) > 200 else ''}
            </div>
            {('<div style="margin-top:6px;">' + ''.join(f'<span style="background:#f0ece0;border:1px solid #d0c8b0;padding:2px 7px;border-radius:4px;font-size:11px;color:#6a5a3a;margin-right:4px;font-family:monospace;">{t}</span>' for t in a.get('tags',[])[:3]) + '</div>') if a.get('tags') else ''}
        </td></tr>"""

    # Byg TED-sektion
    ted_html = ""
    for t in all_ted[:6]:
        val = f" · {t['value']:,.0f} DKK" if t.get('value') else ""
        ted_html += f"""
        <tr><td style="padding:6px 0 14px;border-bottom:1px solid #e8e4d8;">
            <a href="{t.get('url','#')}" style="font-family:Georgia,serif;font-size:14px;
               font-weight:600;color:#1a2a3a;text-decoration:none;display:block;margin-bottom:4px;">
               {t.get('title','')}</a>
            <div style="font-size:11px;color:#6a7a8a;font-family:monospace;">
                {t.get('org','')} · {t.get('date','')[:10]}{val}
            </div>
        </td></tr>"""

    if not ted_html:
        ted_html = '<tr><td style="padding:10px 0;font-size:13px;color:#9a9a8a;">Ingen nye udbud fundet i dag.</td></tr>'

    total_news = len(all_news)
    total_ted = len(all_ted)

    return f"""<!DOCTYPE html>
<html lang="da">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"></head>
<body style="margin:0;padding:0;background:#f5f0e8;font-family:'Helvetica Neue',Arial,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#f5f0e8;padding:40px 20px;">
<tr><td align="center">
<table width="620" cellpadding="0" cellspacing="0" style="max-width:620px;width:100%;">

  <!-- HEADER -->
  <tr><td style="background:#1a3a1a;padding:32px 40px;border-radius:12px 12px 0 0;">
    <div style="font-family:monospace;font-size:10px;letter-spacing:3px;color:#4db87a;
                text-transform:uppercase;margin-bottom:8px;">
        Det Nationale Netværk for Klimatilpasning
    </div>
    <div style="font-family:Georgia,serif;font-size:28px;font-weight:700;color:#f5f0e8;
                letter-spacing:-0.5px;">
        Klimamonitor
    </div>
    <div style="font-family:monospace;font-size:11px;color:#6aaa7a;margin-top:6px;">
        Daglig scanning · {dato}
    </div>
  </td></tr>

  <!-- STATS BAR -->
  <tr><td style="background:#2d5a2d;padding:14px 40px;">
    <table width="100%" cellpadding="0" cellspacing="0">
    <tr>
      <td style="font-family:monospace;font-size:12px;color:#a0d0a0;">
        <strong style="font-size:20px;color:#4db87a;">{total_news}</strong> nyheder
      </td>
      <td style="font-family:monospace;font-size:12px;color:#a0d0a0;">
        <strong style="font-size:20px;color:#4db87a;">{total_ted}</strong> EU-udbud
      </td>
      <td style="font-family:monospace;font-size:12px;color:#a0d0a0;">
        <strong style="font-size:20px;color:#4db87a;">153</strong> kilder scannet
      </td>
    </tr>
    </table>
  </td></tr>

  <!-- BODY -->
  <tr><td style="background:#faf7f2;padding:32px 40px;border-radius:0 0 12px 12px;">

    <!-- NYHEDER -->
    <table width="100%" cellpadding="0" cellspacing="0">
    <tr><td style="padding-bottom:16px;">
      <div style="font-family:Georgia,serif;font-size:20px;font-weight:600;color:#1a3a1a;
                  border-bottom:2px solid #1a3a1a;padding-bottom:10px;">
          Dagens nyheder & projekter
      </div>
    </td></tr>
    {news_html if news_html else '<tr><td style="padding:10px 0;font-size:13px;color:#9a9a8a;">Ingen relevante nyheder fundet i dag.</td></tr>'}
    </table>

    <!-- TED UDBUD -->
    <table width="100%" cellpadding="0" cellspacing="0" style="margin-top:32px;">
    <tr><td style="padding-bottom:16px;">
      <div style="font-family:Georgia,serif;font-size:20px;font-weight:600;color:#1a2a3a;
                  border-bottom:2px solid #1a2a3a;padding-bottom:10px;">
          EU-udbud (TED)
      </div>
    </td></tr>
    {ted_html}
    </table>

    <!-- FOOTER -->
    <table width="100%" cellpadding="0" cellspacing="0" style="margin-top:40px;
           border-top:1px solid #d0c8b0;padding-top:20px;">
    <tr><td style="font-size:11px;color:#9a9a8a;font-family:monospace;line-height:1.8;">
        DNNK Klimamonitor · Automatisk daglig scanning kl. 08:00<br>
        Kilder: Ingeniøren, Altinget, DR, TV2, DMI, GEUS, Miljøstyrelsen,
        Rambøll, COWI, HOFOR, Aarhus Vand m.fl. (153 feeds i alt)<br>
        <a href="{PROXY_BASE}" style="color:#2d7a2d;">Åbn dashboard</a>
    </td></tr>
    </table>

  </td></tr>
</table>
</td></tr>
</table>
</body>
</html>"""

async def send_email(subject: str, html_content: str) -> bool:
    """Send e-mail via SendGrid API"""
    if not SENDGRID_API_KEY:
        print("ADVARSEL: SENDGRID_API_KEY ikke sat – e-mail ikke sendt")
        return False

    payload = {
        "personalizations": [{"to": [{"email": EMAIL_TO}]}],
        "from": {"email": EMAIL_FROM, "name": "DNNK Klimamonitor"},
        "subject": subject,
        "content": [{"type": "text/html", "value": html_content}]
    }

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                "https://api.sendgrid.com/v3/mail/send",
                headers={
                    "Authorization": f"Bearer {SENDGRID_API_KEY}",
                    "Content-Type": "application/json"
                },
                json=payload,
                timeout=15
            )
            if resp.status_code in (200, 202):
                print(f"E-mail sendt til {EMAIL_TO}")
                return True
            else:
                print(f"SendGrid fejl: {resp.status_code} – {resp.text}")
    except Exception as e:
        print(f"E-mail fejl: {e}")
    return False

async def run_daily_digest():
    """Kør den daglige scanning og send digest"""
    dk_tz = timezone(timedelta(hours=1))
    dato = datetime.now(dk_tz).strftime("%d. %B %Y")
    print(f"[{datetime.now(dk_tz).strftime('%H:%M')}] Starter daglig scanning...")

    # Hent data parallelt for alle søgeord
    news_tasks = [fetch_news(q) for q in DEFAULT_QUERIES]
    ted_tasks  = [fetch_ted(q) for q in DEFAULT_QUERIES[:2]]

    all_results = await asyncio.gather(*news_tasks, *ted_tasks)

    news_idx = len(DEFAULT_QUERIES)
    all_news_raw = [a for sublist in all_results[:news_idx] for a in sublist]
    all_ted_raw  = [t for sublist in all_results[news_idx:] for t in sublist]

    # Deduplikér på titel
    seen_titles = set()
    all_news, all_ted = [], []
    for a in all_news_raw:
        t = a.get("title", "")[:60]
        if t not in seen_titles:
            seen_titles.add(t)
            all_news.append(a)
    for t in all_ted_raw:
        ti = t.get("title", "")[:60]
        if ti not in seen_titles:
            seen_titles.add(ti)
            all_ted.append(t)

    # Sortér nyheder efter relevans
    all_news.sort(key=lambda x: x.get("relevance", 0), reverse=True)

    print(f"Fundet {len(all_news)} nyheder og {len(all_ted)} TED-udbud")

    html = build_html_email(all_news, all_ted, dato)
    subject = f"DNNK Klimamonitor · {dato} · {len(all_news)} nyheder, {len(all_ted)} udbud"

    await send_email(subject, html)

async def scheduler_loop():
    """Kør daglig scanning kl. 08:00 dansk tid"""
    dk_tz = timezone(timedelta(hours=1))
    print("Scheduler startet – venter på kl. 08:00...")
    while True:
        now = datetime.now(dk_tz)
        # Beregn næste kl. 08:00
        next_run = now.replace(hour=8, minute=0, second=0, microsecond=0)
        if now >= next_run:
            next_run += timedelta(days=1)
        wait_seconds = (next_run - now).total_seconds()
        print(f"Næste scanning: {next_run.strftime('%d/%m %H:%M')} (om {int(wait_seconds/3600)}t {int((wait_seconds%3600)/60)}m)")
        await asyncio.sleep(wait_seconds)
        await run_daily_digest()

if __name__ == "__main__":
    asyncio.run(run_daily_digest())
