# your_app/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import RideLocation

class RideLocationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.ride_id = self.scope['url_route']['kwargs']['ride_id']
        await self.channel_layer.group_add(f"ride_{self.ride_id}", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(f"ride_{self.ride_id}", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        latitude = data['latitude']
        longitude = data['longitude']

        await self.save_location(latitude, longitude)

        await self.channel_layer.group_send(
            f"ride_{self.ride_id}",
            {
                'type': 'location_update',
                'latitude': latitude,
                'longitude': longitude,
            }
        )

    async def location_update(self, event):
        await self.send(text_data=json.dumps({
            'latitude': event['latitude'],
            'longitude': event['longitude'],
        }))

    @sync_to_async
    def save_location(self, latitude, longitude):
        RideLocation.objects.create(ride=self.ride_id, latitude=latitude, longitude=longitude)
