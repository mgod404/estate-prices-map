from bs4 import BeautifulSoup
from requests import get
from decimal import *
from forex_python.converter import CurrencyRates
import json
import concurrent.futures


def how_many_pages_to_scrape(URL):

    URL = URL + '1'

    request = get(URL)
    html = request.content
    page = BeautifulSoup(html, 'html.parser')
    data = str(page.find('script', id="__NEXT_DATA__").contents[0])
    data_json = json.loads(data)
    page_count = data_json['props']['pageProps']['tracking']['listing']['page_count']

    return int(page_count)


def otodom_page_scraper(number_of_page_to_scrape, URL):

    URL = URL + str(number_of_page_to_scrape)
    array_of_offers_scraped = []

    request = get(URL)
    html = request.content
    page = BeautifulSoup(html, 'html.parser')
    data = str(page.find('script', id="__NEXT_DATA__").contents[0])
    data_json = json.loads(data)

    offers = data_json['props']['pageProps']['data']['searchAds']['items']
    for offer in offers:

        try: 
            price = offer['totalPrice']['value']
            currency = offer['totalPrice']['currency']
        except TypeError:
            continue

        if currency != 'PLN':
            c = CurrencyRates()
            exchange_rate = c.get_rate(currency, 'PLN')
            price = price * exchange_rate
        
        try:
            size = offer['areaInSquareMeters']
        except TypeError:
            continue

        pricesqm = int(Decimal(price) / Decimal(size))

        location = offer['locationLabel']['value']
        location_splitted = location.split(',')
        if len(location_splitted) <= 2:
            continue
        
        link = 'https://www.otodom.pl/pl/oferta/' + offer['slug']

        picture = offer['images'][0]['thumbnail']

        array_of_offers_scraped.append({
            'location': location, 
            'pricesqm': pricesqm, 
            'price': price, 
            'size': size, 
            'link': link, 
            'picture': picture
        })
    # print(f'page {number_of_page_to_scrape} done')
    return array_of_offers_scraped


def get_lowest_price(raw_list):
    distinct_locations = set(item['location'] for item in raw_list)
    min_price_list = []

    for item in distinct_locations:
        x = [i for i in raw_list if i['location'] == item]
        x.sort(key=lambda d: d['pricesqm'])
        min_price_list.append(x[0])
    return min_price_list


def otodom_web_scraper(URL):

    results = []

    how_many_pages = range(1,how_many_pages_to_scrape(URL) + 1)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(lambda m: results.extend(otodom_page_scraper(m, URL)), how_many_pages)

    return get_lowest_price(results)

