from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from ExternalAPI.extract_lat_lng import ors_get_coordinates


def get_geocode(address):
    geolocator = Nominatim(user_agent="my_route_optimizer")
    try:
        location = geolocator.geocode(address)
        if location:
            return f"{location.longitude}, {location.latitude}"
        location = ors_get_coordinates(address)
        if location:
            return f"{location[0]}, {location[1]}"

        raise ValueError(f"Could not find coordinates for address: {address}")
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        raise ValueError(f"Geocoding service error: {str(e)}")


