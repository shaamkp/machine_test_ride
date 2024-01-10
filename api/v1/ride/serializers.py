from rest_framework import serializers
from ride.models import Ride, RideLocation


class CreateRideSerializer(serializers.Serializer):
    pick_up_location = serializers.CharField()
    dropoff_location = serializers.CharField()


class ListRideSerializer(serializers.ModelSerializer):
    driver = serializers.SerializerMethodField()
    rider = serializers.SerializerMethodField()

    class Meta:
        model = Ride
        fields = (
            'id',
            'driver',
            'rider',
            'pick_up_location',
            'dropoff_location',
            'status'
        )

    def get_driver(self, instance):
        if instance.driver:
            return instance.driver.name
        else:
            return None
        
    def get_rider(self, instance):
        if instance.rider:
            return instance.rider.name
        else:
            return None
        

class UpdateRideLocationSerializer(serializers.Serializer):
    latitude = serializers.CharField()
    longitude = serializers.CharField()


class RideLocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = RideLocation
        fields = (
            'id',
            'latitude',
            'longitude',
            'timestamp',

        )


class ConfirmRideSerializer(serializers.Serializer):
    ride_id = serializers.CharField()
    is_confirm = serializers.CharField()