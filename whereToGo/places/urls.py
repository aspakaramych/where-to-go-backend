from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_map, name='map'),
    path('places/', views.all_places_geojson, name='places_list'),
    path('places/<int:place_id>/', views.place_details_endpoint, name='place_details')
]