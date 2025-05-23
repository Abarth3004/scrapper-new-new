import requests
from bs4 import BeautifulSoup
from filters import is_valid_job

def scrape_jobandtalent():
    jobs = []
    headers = {"User-Agent": "Mozilla/5.0"}
    for page in range(1, 4):
        url = f"https://jobandtalent.com/es/jobs/search?q=marketing&location=Madrid&page={page}"
        resp = requests.get(url, headers=headers)
        print(f"[JOBANDTALENT] Page {page} - Status {resp.status_code}")
        if resp.status_code != 200:
            break
        soup = BeautifulSoup(resp.text, "html.parser")
        cards = soup.select("div.job")
        print(f"[JOBANDTALENT] Page {page} - Cards: {len(cards)}")
        for card in cards:
            title_tag = card.select_one("h3")
            company = "Jobandtalent"
            summary = card.get_text(" ", strip=True)
            if not title_tag:
                continue
            title = title_tag.get_text(strip=True)
            combined = f"{title} {summary}"
        if is_valid_job(combined, title=title, location="Madrid"):
                jobs.append({
                    "source": "Jobandtalent",
                    "title": title,
                    "company": company,
                    "location": "Madrid",
                    "summary": summary,
                    "url": url
                })
    return jobs