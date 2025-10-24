from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from placesService.models import Place, Image


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

    return JsonResponse(geojson, safe=False, json_dumps_params={'ensure_ascii': False})


def place_details_endpoint(request, place_id):
    place = get_object_or_404(Place, pk=place_id)

    image_urls = [image.image.url for image in place.images.all().order_by('sort_order')]

    place_json = {
        "title": place.title.strip(),
        "imgs": image_urls,
        "description_short": place.description_short,
        "description_long": place.description_long,
        "coordinates": {
            "lng": place.lon,
            "lat": place.lat
        }
    }
    return JsonResponse(place_json, json_dumps_params={'ensure_ascii': False})