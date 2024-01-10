from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from .consumer import RideLocationConsumer

websocket_urlpatterns = [
    path('ws/rides/<int:ride_id>/', RideLocationConsumer.as_asgi()),
]