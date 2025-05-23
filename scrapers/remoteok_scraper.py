import requests
from bs4 import BeautifulSoup
from filters import is_valid_job

def scrape_remoteok():
    url = "https://remoteok.com/remote-marketing-jobs"
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")
    jobs = []
    rows = soup.select("tr.job")
    print(f"[REMOTEOK] Jobs found: {len(rows)}")
    for row in rows:
        title = row.select_one("td.position h2")
        company = row.select_one("td.company h3")
        if not title or not company:
            continue
        title_text = title.get_text(strip=True)
        company_text = company.get_text(strip=True)
        url = "https://remoteok.com" + row.get("data-href", "")
        summary = title_text
        combined = f"{title_text} {summary}"
        if is_valid_job(combined, title=title, location="Remote"):
            jobs.append({
                "source": "RemoteOK",
                "title": title_text,
                "company": company_text,
                "location": "Remote",
                "summary": summary,
                "url": url
            })
    return jobs