from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from placesService.models import Place


def show_map(request):
    return render(request, 'index.html')

def all_places_geojson(request):
    places = Place.objects.all()

    geojson_features = []

    for place in places:
        geojson_features.append({
            'type': 'Feature',
            "geometry": {
                "type": "Point",
                "coordinates": [place.lon, place.lat]
            },
            "properties": {
                "title": place.title,
                "placeId": place.id,
                "detailsUrl": f'/places/{place.id}'
            }
        })

    geojson = {
        "type": "FeatureCollection",
        "features": geojson_features
    }

    return JsonResponse(geojson, safe=False)


def place_details_endpoint(request, place_id):
    place = get_object_or_404(Place, pk=place_id)

    return JsonResponse({"title": place.title}, safe=False)