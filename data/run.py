import sys
from scraper import Scraper

target_url = "https://www.cafe-athome.com/maids"
# target_url = "https://www.cafe-athome.com/graduates/"
dst_path = "maids"

def main():
    active_scraper = Scraper(target_url, dst_path)
    active_scraper.scraping()

if __name__ == "__main__":
    main()
