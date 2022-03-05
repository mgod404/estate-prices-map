from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from .models import Offer, LocationData
from .googlemapsgeocoding import geocode_single_location
from datetime import date
import concurrent.futures 
import json
import ast

def remove_polish_lowercase_chars(word):
    polish_chars_as_english = {
    'ą':'a',
    'ć':'c',
    'ę':'e',
    'ł':'l',
    'ń':'n',
    'ó':'o',
    'ś':'s',
    'ź':'z',
    'ż':'z'
    }
    word = list(word)
    for id,char in enumerate(word):
        if char in polish_chars_as_english:
            word[id] = polish_chars_as_english[char]
    return ''.join(word)


def queryset_to_list_of_dicts(queryset):
    return list(map(lambda q: {
            'location': q.location_data.location, 
            'pricesqm': float(q.pricesqm), 
            'price': float(q.price), 
            'size': float(q.size), 
            'link': q.link, 
            'picture': q.picture,
            'lat': float(q.location_data.latitude),
            'lng': float(q.location_data.longtitude)
        },
        queryset
        ))


def handle_get_request(request):
    request_data = request.GET
    city = remove_polish_lowercase_chars(str(request_data['city']).lower())
    headers={'Access-Control-Allow-Origin': 'http://localhost:8080'}

    if 'city' not in request_data:
        return HttpResponse(status=400, headers=headers)
    
    if not LocationData.objects.filter(city=city).exists():
        return HttpResponse('ERROR: Wrong city name or city not in database',status=400, headers=headers)
    response_offers = Offer.objects.select_related('location_data').filter(
        location_data__city=city,
        date_of_scraping=date.today()
        )
    response_offers_as_list_of_dicts = queryset_to_list_of_dicts(response_offers)

    return JsonResponse(response_offers_as_list_of_dicts, safe=False, headers=headers)


def handle_post_request(request):
    request_data = ast.literal_eval(json.loads(request.body))
    # print(f'Data from POST request :  {request_data}')

    if request_data['key'] != '1234':
        return HttpResponse(status=401)

    if 'data' not in request_data:
        return HttpResponse(status=400)

    city = remove_polish_lowercase_chars(str(request_data['city']).lower())

    for offer in request_data['data']:
        location = str(offer['location']).lower()

        if LocationData.objects.filter(location=location).exists():
            geodata = LocationData.objects.get(location=location)
            print('geodata used from database')
        else:
            geodata = geocode_single_location(location)
            new_geodata = LocationData(
                city= city, 
                location = location, 
                latitude = geodata['lat'],
                longtitude = geodata['lng']
                )
            new_geodata.save()
            print('new geodata created')

        new_offer = Offer(
            location_data = LocationData.objects.get(location=location), 
            pricesqm = offer['pricesqm'], 
            price = offer['price'], 
            size = offer['size'], 
            link = offer['link'], 
            picture = offer['picture'],
        )
        new_offer.save()
        print('new offer saved')

    return HttpResponse(status=200)  


@csrf_exempt
def index(request):
    if request.method == 'GET':
        return handle_get_request(request=request)

    if request.method == 'POST': 
        return handle_post_request(request=request)

    else:
        return HttpResponse(status=418)