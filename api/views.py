from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.serializers import CostEfficientRouteSerializer
from ExternalAPI.route_service import route_coordinate
from api.calculate_fuel_stops import calculate_fuel_stops
from api.get_geocode import get_geocode


class CostEfficientRoute(APIView):

    def get_serializer(self):
        return CostEfficientRouteSerializer()

    def get(self, request):
        return Response({"message": "Please provide 'start' and 'end' locations."})

    def post(self, request, *args, **kwargs):
        from timeit import default_timer as timer
        start = timer()
        start_location, end_location = None, None
        serializer = CostEfficientRouteSerializer(data=request.data)
        if serializer.is_valid():
            start_location = serializer.validated_data["start"]
            end_location = serializer.validated_data["end"]

        if not start_location or not end_location:
            return Response({"error": "Start and end locations are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Step 1: Get the Geo Coordinates using Nominatim
        try:
            start_coords = get_geocode(start_location)
            end_coords = get_geocode(end_location)
            print(start_coords, end_coords)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

        try:
            # Step 2: Get the route from OpenRouteService
            route = route_coordinate(start_coords, end_coords)
        except Exception as e:
            return Response({"error": str(e)}, status="404")

        if not route:
            return Response({"error": "Could not calculate the route"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Step 3: Calculate fuel stops and total cost
        fuel_stops, total_cost = calculate_fuel_stops(route)
        end = timer()
        print(end - start)

        # Step 4: Return the response
        return Response({
            "start_location": start_location,
            "end_location": end_location,
            "total_cost": f"${total_cost:.2f}",
            "total_distance": f"{int(route['properties']['segments'][0]['distance'] / 1609.34)} miles",
            "fuel_stops": fuel_stops,
        })
