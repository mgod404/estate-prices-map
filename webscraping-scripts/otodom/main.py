from otodomestateprices import otodom_web_scraper, otodom_page_scraper
import datetime
import json
from requests import get
from bs4 import BeautifulSoup


if __name__ == "__main__":

    req = get('http://127.0.0.1:8000/api/', params={'city' : 'debica'})
    print(req.status_code)
    response_list = req.json()
    print(response_list[1])