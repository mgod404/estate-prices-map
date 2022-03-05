import requests
import concurrent.futures

API_KEY = 'AIzaSyCHCXxiYJ-CjqHWR4MEZQplN_vwiuqPpfE'
base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'

def geocode_single_location(location):
    # address = str(row['location'])
    row = {'location': location}
    address = location
    params = {'key': API_KEY, 'address': address}
    response = requests.get(base_url, params=params).json()
    response.keys()

    if response['status'] == 'OK':
        geometry = response['results'][0]['geometry']
        row['lat'] = geometry['location']['lat']
        row['lng'] = geometry['location']['lng']
        return row

    if response['status'] == 'REQUEST_DENIED':
        print("Request to Geocoding API is denied, issue with API key")


# def geocode_data(data):
# to make this code work change input variable in geocode_single_location to 'row'

#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         executor.map(geocode_single_location, list(data))
#     print(str(data))
#     return data
