from otodomestateprices import otodom_web_scraper, otodom_page_scraper, how_many_pages_to_scrape
from requests import post
import json
import sys
import time
import os
import schedule

def check_if_scraper_works():
    TEST_URL = "https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/warszawa?limit=10&page=1"
    page_count = how_many_pages_to_scrape(TEST_URL)
    if type(page_count) != int or page_count <= 0:
        print('page count does not work properly')
        return False
    scraping_results = otodom_page_scraper(1,TEST_URL)
    if len(scraping_results) <= 1:
        print('scraping results are broken')
        return False
    print('Scraper passed the test')
    return True


def post_data(city, results):
    payload = {"key" : '1234','city': city, 'data' : results}
    print(f'Length is {len(results)}')
    data = json.dumps(payload)
    print(f'json data in memory {sys.getsizeof(data)}')
    r = post(f"http://estateprices.martyngodlewski.com/api/", json=data)
    print(str(f'Status code {r.status_code}'))


def get_new_offers(cities):
    for city,url in cities.items():
        print(url)
        print(city)
        results = otodom_web_scraper(url)
        post_data(city, results)


if __name__ == "__main__":

    CITIES_URL = {
        'warszawa' : "https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/warszawa?limit=100&page=",
        'krakow' : "https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/krakow?limit=100&page=",
        'wroclaw' : "https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/wroclaw?limit=100&page="
    }

    current_time = time.strftime("%H:%M:%S", time.localtime())
    print(current_time)

    def webscrape():
        current_time = time.strftime("%H:%M:%S", time.localtime())
        print(current_time)
        if not check_if_scraper_works():
            sys.exit("Webscraper stopped functioning properly. Possible changes at the scraped site")
        get_new_offers(cities=CITIES_URL)

    schedule.every().day.at("15:59").do(webscrape)


    while True:
        schedule.run_pending()
        time.sleep(1)
