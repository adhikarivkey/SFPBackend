import requests
from AdminPanel.settings.base import ORS_TOKEN


def route_coordinate(start, end):
    try:
        url = f"https://api.openrouteservice.org/v2/directions/driving-car"
        headers = {'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
                   "Authorization": ORS_TOKEN}
        params = {
            "start": start,
            "end": end,
            'geometry_format': 'geojson'
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()["features"][0]
        return None
    except:
        return None
