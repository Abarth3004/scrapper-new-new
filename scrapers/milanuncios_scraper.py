import requests
from bs4 import BeautifulSoup
from filters import is_valid_job

def scrape_milanuncios():
    jobs = []
    headers = {"User-Agent": "Mozilla/5.0"}
    for page in range(1, 4):
        url = f"https://www.milanuncios.com/ofertas-de-empleo-en-madrid/?pagina={page}&buscador=marketing"
        resp = requests.get(url, headers=headers)
        print(f"[MILANUNCIOS] Page {page} - Status {resp.status_code}")
        if resp.status_code != 200:
            break
        soup = BeautifulSoup(resp.text, "html.parser")
        cards = soup.select("div.aditem")
        print(f"[MILANUNCIOS] Page {page} - Cards: {len(cards)}")
        for card in cards:
            title_tag = card.select_one("a.aditem-detail-title")
            company = "N/A"
            summary = card.get_text(" ", strip=True)
            if not title_tag:
                continue
            title = title_tag.get_text(strip=True)
            url = "https://www.milanuncios.com" + title_tag.get("href")
            combined = f"{title} {summary}"
        if is_valid_job(combined, title=title, location="Madrid"):
                jobs.append({
                    "source": "Milanuncios",
                    "title": title,
                    "company": company,
                    "location": "Madrid",
                    "summary": summary,
                    "url": url
                })
    return jobs