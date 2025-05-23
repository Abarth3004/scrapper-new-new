import requests
from bs4 import BeautifulSoup
from filters import is_valid_job

def scrape_infojobs():
    jobs = []
    headers = {"User-Agent": "Mozilla/5.0"}
    for page in range(1, 4):
        url = f"https://www.infojobs.net/jobsearch/search-results/list.xhtml?keyword=marketing&province=Madrid&page={page}"
        resp = requests.get(url, headers=headers)
        print(f"[INFOJOBS] Page {page} - Status {resp.status_code}")
        if resp.status_code != 200:
            break
        soup = BeautifulSoup(resp.text, "html.parser")
        cards = soup.select("article.js-job-item")
        print(f"[INFOJOBS] Page {page} - Cards: {len(cards)}")
        for card in cards:
            title_tag = card.select_one(".js-offer-title")
            company = card.select_one(".js-offer-company")
            url_tag = title_tag if title_tag else None
            summary = card.get_text(" ", strip=True)
            if not title_tag or not url_tag:
                continue
            title = title_tag.get_text(strip=True)
            job_url = "https://www.infojobs.net" + url_tag.get("href")
            combined = f"{title} {summary}"
        if is_valid_job(combined, title=title, location="Madrid"):
                jobs.append({
                    "source": "InfoJobs",
                    "title": title,
                    "company": company.get_text(strip=True) if company else "",
                    "location": "Madrid",
                    "summary": summary,
                    "url": job_url
                })
    return jobs