from scrapers.infojobs_scraper import scrape_infojobs
from scrapers.milanuncios_scraper import scrape_milanuncios
from scrapers.remoteok_scraper import scrape_remoteok
from scrapers.jobandtalent_scraper import scrape_jobandtalent
from export_excel import export_jobs_to_excel

def main():
    all_jobs = []
    all_jobs += scrape_infojobs()
    all_jobs += scrape_milanuncios()
    all_jobs += scrape_remoteok()
    all_jobs += scrape_jobandtalent()
    export_jobs_to_excel(all_jobs)

if __name__ == "__main__":
    main()