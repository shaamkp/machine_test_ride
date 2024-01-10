from django.urls import path, re_path
from . import views
from ride.consumer import RideLocationConsumer


app_name = "api_v1_ride"

urlpatterns = [
    re_path(r'^request-ride/$', views.create_ride, name="request-ride"),
    re_path(r'^list-rides/$', views.list_rides, name="list-rides"),
    re_path(r'^list-ride/(?P<pk>.*)/$', views.list_ride, name="list-ride"),
    re_path(r'^update-ride-location/(?P<pk>.*)/$', views.update_ride_location, name="update-ride-location"),
    re_path(r'^track-ride-location/(?P<pk>.*)/$', views.track_ride_location, name="track-ride-location"),

    re_path(r'^ride-confirmation/$', views.ride_confirmation, name="ride-confirmation"),

    
]

websocket_urlpatterns = [
    path('ws/rides/<int:ride_id>/', RideLocationConsumer.as_asgi()),
]