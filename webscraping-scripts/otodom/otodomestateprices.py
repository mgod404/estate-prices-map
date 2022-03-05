from bs4 import BeautifulSoup
from requests import get
from decimal import *
import re
import json
import concurrent.futures

def how_many_pages_to_scrape(URL):

    page = get(URL)
    bs = BeautifulSoup(page.content, 'html.parser')
    page_params = str(bs.find('script', id="__NEXT_DATA__"))
    find_page_count = page_params.find('totalPages')

    page_count = ""
    for char in page_params[find_page_count+12:find_page_count+20]:
        if char.isdigit():
            page_count= page_count + char
        if char == ',':
            break
    return int(page_count)

def otodom_page_scraper(number_of_page_to_scrape, URL):

    array_of_offers_scraped = []

    URL = URL + str(number_of_page_to_scrape)

    page = get(URL)
    bs = BeautifulSoup(page.content, 'html.parser')
    body = bs.find('div', class_='css-1sxg93g e76enq86')
    offers = body.find_all('li', class_='css-p74l73 es62z2j26')


    for offer in offers:
        price = offer.find_all('p', class_='css-1bq5zfe es62z2j16')[0].get_text()
        price = ''.join(re.findall(r"[-+]?\d*\.|,\d+|\d+", price))
        if price == '':
            continue
        
        
        size = offer.find_all('span', class_='css-1q7zgjd eclomwz0')[1].get_text()
        size = ''.join(re.findall(r"[-+]?\d*\.|,\d+|\d+", size))
        if size == '':
            continue
        
        pricesqm = int( Decimal(price) / Decimal(size) ) 

        location = offer.find('span', class_='css-17o293g es62z2j18').get_text()
        location_splitted = location.split(', ')
        if len(location_splitted) <= 2:
            continue
        link = offer.find('a', class_='css-1c4ocg7 es62z2j23')['href']
        link = "https://www.otodom.pl" + link
        picture = offer.find('img')['src']
        array_of_offers_scraped.append({
            'location': location, 
            'pricesqm': pricesqm, 
            'price': price, 
            'size': size, 
            'link': link, 
            'picture': picture
            })
    print(f'page {number_of_page_to_scrape} scraped')
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

