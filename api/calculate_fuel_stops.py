from api.models import GasStation
from geopy.distance import geodesic
import numpy as np

MILES_PER_GALLON = 10
MAX_RANGE = 500


def calculate_fuel_stops(route):
    coordinates = np.array(route['geometry']['coordinates'])
    total_distance = route['properties']['segments'][0]['distance'] / 1609.34  # meters to miles

    # Pre-calculate cumulative distances along the route
    cum_distances = [0.0]
    for i in range(1, len(coordinates)):
        dist = geodesic(coordinates[i - 1][::-1], coordinates[i][::-1]).miles
        cum_distances.append(cum_distances[-1] + dist)

    current_position = 0.0
    fuel_remaining = MAX_RANGE
    total_cost = 0.0
    fuel_stops = []

    while current_position + fuel_remaining < total_distance:
        search_start = current_position
        search_end = min(current_position + MAX_RANGE, total_distance)

        # Find stations in current search window using binary search
        start_idx = np.searchsorted(cum_distances, search_start, side='right') - 1
        end_idx = np.searchsorted(cum_distances, search_end, side='right')

        # Get bounding box of current route segment
        segment_coords = coordinates[start_idx:end_idx + 1]
        min_lat, max_lat = segment_coords[:, 1].min(), segment_coords[:, 1].max()
        min_lon, max_lon = segment_coords[:, 0].min(), segment_coords[:, 0].max()

        # Expand bbox by 1 degree (~69 miles) for safety
        stations = GasStation.objects.filter(
            lat__range=(min_lat - 1, max_lat + 1),
            lng__range=(min_lon - 1, max_lon + 1)
        )

        # Find viable stations within remaining range
        viable_stations = []
        for station in stations:
            # Find nearest point on route
            idx = np.argmin(np.sum((coordinates - [station.lng, station.lat]) ** 2, axis=1))
            station_mile = cum_distances[idx]

            if (station_mile > current_position and
                    station_mile <= current_position + fuel_remaining and
                    geodesic((station.lat, station.lng),
                             (coordinates[idx][1], coordinates[idx][0])).miles <= 10):
                viable_stations.append((station, station_mile))

        if not viable_stations:
            raise ValueError(f"No stations found between {current_position} and {search_end} miles")

        # Select cheapest station (prefer later stations with same price)
        viable_stations.sort(key=lambda x: (x[0].price, -x[1]))
        best_station, station_mile = viable_stations[0]

        # Calculate fuel needed
        distance_to_station = station_mile - current_position
        fuel_used = distance_to_station / MILES_PER_GALLON
        fuel_needed = (MAX_RANGE / MILES_PER_GALLON) - (fuel_remaining / MILES_PER_GALLON - fuel_used)
        refuel_cost = fuel_needed * best_station.price

        fuel_stops.append({
            "name": best_station.name,
            "mile_marker": round(station_mile, 2),
            "cost": round(refuel_cost, 2),
            "lat": best_station.lat,
            "lng": best_station.lng,
            "map_url": f"https://www.openstreetmap.org/?mlat={best_station.lat}&mlon={best_station.lng}"
        })

        total_cost += refuel_cost
        current_position = station_mile
        fuel_remaining = MAX_RANGE - (station_mile - current_position)

    return fuel_stops, round(total_cost, 2)