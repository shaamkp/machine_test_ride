from django.contrib import admin
from ride.models import *

class RideAdmin(admin.ModelAdmin):
    list_display = ('id', 'driver', 'rider', 'pick_up_location', 'dropoff_location')

admin.site.register(Ride, RideAdmin)


class RideLocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'ride', 'latitude', 'longitude', 'timestamp')

admin.site.register(RideLocation, RideLocationAdmin)
