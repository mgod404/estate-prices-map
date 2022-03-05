from requests import get, post, session
from bs4 import BeautifulSoup
import json
from googlemapsgeocoding import geocode_single_location
from otodomestateprices import otodom_web_scraper,otodom_page_scraper, how_many_pages_to_scrape

city = 'warszawa'
x = "https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/warszawa?page="

results = otodom_web_scraper(x)

print(str(results))

payload = {"key" : '1234','city': city, 'data' : results}

data = json.dumps(payload)

r = post('http://127.0.0.1:8000/api/', json=data)
print(str(r.status_code))
