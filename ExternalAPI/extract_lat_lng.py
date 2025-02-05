import requests
from api.models import GasStation
from AdminPanel.settings.base import GOMAPS_API_KEY, ORS_TOKEN


def gomap_gas_station_lat_lon(name, city, state, serial, truckstop_id):
    address = f"{name}, {city}, {state}"
    params = {
        "address": address,
        "key": GOMAPS_API_KEY
    }
    response = requests.get("https://maps.gomaps.pro/maps/api/geocode/json", params=params)
    if response.status_code == 200:
        data = response.json()
        gas_stations = []
        for result in data.get("results", []):
            if "gas_station" in result.get("types", []):
                lat = result["geometry"]["location"]["lat"]
                lon = result["geometry"]["location"]["lng"]
                formatted_address = result["formatted_address"]
                gas_stations.append({
                    "name": name,
                    "id": serial,
                    "stop_id": truckstop_id,
                    "formatted_address": formatted_address,
                    "latitude": lat,
                    "longitude": lon
                })

        return gas_stations if gas_stations else None
    else:
        print(response.status_code, serial, truckstop_id)
    return None


def osm_gas_station_lat_lon_2(name, city, state, serial, truckstop_id):
    address = f"{name}, {city}, {state}"
    params = {
        "q": address,
        "format": "json",
        "addressdetails": 1
    }
    try:
        response = requests.get("https://nominatim.openstreetmap.org/search",
                                params=params, headers={'User-Agent': 'MyGeocodingApp/1.0 (your-contact@example.com)'},
                                timeout=10)

        if response.status_code == 200:
            data = response.json()
            gas_stations = []
            for result in data:
                if result.get('class') == 'amenity' and result.get('type') == 'fuel':
                    gas_stations.append({
                        "name": name,
                        "id": serial,
                        "stop_id": truckstop_id,
                        "formatted_address": result.get('display_name', ''),
                        "latitude": float(result['lat']),
                        "longitude": float(result['lon'])
                    })

            return gas_stations if gas_stations else None

        else:
            print(f"Error {response.status_code} for {serial}-{truckstop_id}")
            return None

    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Request failed for {serial}-{truckstop_id}: {str(e)}")
        return None


def ors_get_coordinates(place):

    url = f"https://api.openrouteservice.org/geocode/search"
    params = {"api_key": ORS_TOKEN, "text": place}

    response = requests.get(url, params=params).json()

    if response.get("features"):
        return response["features"][0]["geometry"]["coordinates"]  # Returns [longitude, latitude]
    return None


count, fail, number = 0, 0, 0
station = []  # GasStation.objects.filter(comment='Not Found').order_by('id').values('name', 'city', 'state',
              # 'truckstop_id', 'id')

for i in station:
    gas_station_data = gomap_gas_station_lat_lon(i['name'], i['city'], i['state'], i['id'], i['truckstop_id'])
    if gas_station_data:
        for station in gas_station_data:
            (GasStation.objects.filter(id=station['id'], truckstop_id=station['stop_id']).
             update(map_address=station['formatted_address'], lat=station['latitude'], lng=station['longitude'],
                    comment='Found'))
        count += 1
    else:
        fail += 1

    print(number)
    number += 1

print(count, fail)
