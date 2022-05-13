from decimal import Decimal
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Offer, LocationData
from datetime import date
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

    if 'city' not in request_data:
        return HttpResponse(status=400)
    
    if not LocationData.objects.filter(city=city).exists():
        return HttpResponse('ERROR: Wrong city name or city not in database',status=400)
    response_offers = Offer.objects.select_related('location_data').filter(
        location_data__city=city,
        date_of_scraping=date.today()
        )
    print(len(response_offers))
    response_offers_as_list_of_dicts = queryset_to_list_of_dicts(response_offers)
    print('hello')
    return JsonResponse(response_offers_as_list_of_dicts, safe=False)


def handle_post_request(request):
    request_data = ast.literal_eval(json.loads(request.body))

    if request_data['key'] != '1234':
        return HttpResponse(status=401)

    if 'data' not in request_data:
        return HttpResponse(status=400)

    city = remove_polish_lowercase_chars(str(request_data['city']).lower())

    for offer in request_data['data']:
        location = str(offer['location']).lower()

        if LocationData.objects.filter(location=location).exists():
            geodata = LocationData.objects.get(location=location)
            # print('geodata used from database')
        else:
            geodata = {
                'lat': offer['lat'],
                'lng': offer['lng']
            }
            new_geodata = LocationData(
                city= city, 
                location = location,
                latitude = geodata['lat'],
                longtitude = geodata['lng']
                )
            try:
                new_geodata.save()
            except:
                print(new_geodata)
            print('new geodata created')

        new_offer = Offer(
            location_data = LocationData.objects.get(location=location), 
            pricesqm = Decimal(offer['pricesqm']), 
            price = Decimal(offer['price']), 
            size = Decimal(offer['size']), 
            link = offer['link'], 
            picture = offer['picture'],
        )
        print(f"{offer['price']} , {offer['size'], offer['pricesqm']}")
        new_offer.save()
        # print('new offer saved')
    
    Offer.objects.exclude(date_of_scraping=date.today()).delete()

    return HttpResponse(status=200)  


@csrf_exempt
def index(request):
    if request.method == 'GET':
        return handle_get_request(request=request)

    if request.method == 'POST': 
        return handle_post_request(request=request)

    else:
        return HttpResponse(status=418)


def queryset_to_list_of_dicts_geodata(queryset):
    return list(map(lambda q: {
            'city': q.city,
            'location': q.location,
            'latitude': q.latitude,
            'longtitude': q.longtitude
        },
        queryset
        ))

@csrf_exempt
def geo_data(request):
    if request.method == 'GET':
        request_data = request.GET
        if 'city' not in request_data:
            return HttpResponse(status=400)
        city = remove_polish_lowercase_chars(str(request_data['city']).lower())
        geo_data = LocationData.objects.filter(city=city)
        geo_data_serialized = queryset_to_list_of_dicts_geodata(geo_data)
        return JsonResponse(geo_data_serialized, safe=False)




