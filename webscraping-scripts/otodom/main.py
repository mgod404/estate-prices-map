from otodomestateprices import otodom_web_scraper, otodom_page_scraper, how_many_pages_to_scrape
from requests import post
import json
import sys
import time
import os
import schedule

def check_if_scraper_works():
    TEST_URL = "https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/warszawa?limit=10&page="
    page_count = how_many_pages_to_scrape(TEST_URL)
    if type(page_count) != int or page_count > 0:
        return False
    scraping_results = otodom_page_scraper(1,TEST_URL)
    if len(scraping_results) <= 1:
        return False
    return True


def post_data(city, results):
    payload = {"key" : '1234','city': city, 'data' : results}
    data = json.dumps(payload)
    print(f"http://{os.environ.get('BACKEND_URL')}/api/")
    r = post(f"http://127.0.0.1:8000/api/", json=data)
    print(str(r.status_code))


def get_new_offers(CITIES_URL):
    for city,url in CITIES_URL.items():
        print(url)
        print(city)
        results = otodom_web_scraper(url)
        post_data(city, results)


if __name__ == "__main__":

    CITIES_URL = {
        'warszawa' : "https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/warszawa?limit=500&page=",
        'krakow' : "https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/krakow?limit=100&page=",
        'wroclaw' : "https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/wroclaw?limit=100&page="
    }

    schedule.every().day.at("02:00").do(get_new_offers(CITIES_URL))

    while True:
        if not check_if_scraper_works:
            sys.exit("Webscraper stopped functioning properly. Possible changes at the scraped site")
        schedule.run_pending()
        time.sleep(1)