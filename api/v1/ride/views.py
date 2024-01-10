import traceback

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from django.db import transaction

from general.functions import generate_serializer_errors
from accounts.models import *
from ride.models import *
from api.v1.ride.serializers import *
from general.decorators import group_required




@api_view(['POST'])
@group_required(['RiderProfile'])
def create_ride(request):
    try:
        transaction.set_autocommit(False)
        user = request.user
        serialized_data = CreateRideSerializer(data=request.data)
        if serialized_data.is_valid():
            pick_up_location = request.data["pick_up_location"]
            dropoff_location = request.data["dropoff_location"]

            if (profile := RiderProfile.objects.filter(user=user)).exists():
                profile = profile.latest('date_added')

                if (driver := DriverProfile.objects.filter(status='available', is_deleted=False)).exists():
                    driver = driver.order_by('?').first()

                    ride = Ride.objects.create(
                        driver = driver,
                        rider = profile,
                        pick_up_location = pick_up_location,
                        dropoff_location = dropoff_location
                    )

                    transaction.commit()
                    response_data = {
                        "StatusCode" : 6000,
                        "data" : {
                            "title" : "Success",
                            "message" : "Ride created successfully and Driver will pick you"
                        }
                    }
                else:
                    response_data = {
                        "StatusCode": 6001,
                        "data" : {
                            "title" : "Failed",
                            "message" : "No driver found",
                        }
                    }
            else:
                response_data = {
                    "StatusCode": 6001,
                    "data" : {
                        "title" : "Failed",
                        "message" : "profile not found",
                    }
                }
        else:
            response_data = {
                "StatusCode" : 6001,
                "data" : {
                    "title" : "Failed",
                    "message" : generate_serializer_errors(serialized_data._errors)
                }
            }
        
    except Exception as e:
        transaction.rollback()
        errType = e.__class__.__name__
        errors = {
            errType: traceback.format_exc()
        }
        response_data = {
            "status": 0,
            "api": request.get_full_path(),
            "request": request.data,
            "message": str(e),
            "response": errors
        }

    return Response({'app_data': response_data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@group_required(['RiderProfile', 'DriverProfile'])
def list_rides(request):
    try:
        if (rides := Ride.objects.filter(is_deleted=False)).exists():

            serialized_data = ListRideSerializer(
                rides,
                context = {
                    "request" : request
                },
                many = True
            ).data

            response_data = {
                "StatusCode" : 6000,
                "data" : serialized_data
            }
        else:
            response_data = {
                "StatusCode" : 6001,
                "data" : []
            }
    except Exception as e:
        transaction.rollback()
        errType = e.__class__.__name__
        errors = {
            errType: traceback.format_exc()
        }
        response_data = {
            "status": 0,
            "api": request.get_full_path(),
            "request": request.data,
            "message": str(e),
            "response": errors
        }

    return Response({'app_data': response_data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@group_required(['RiderProfile', 'DriverProfile'])
def list_ride(request, pk):
    try:
        if (rides := Ride.objects.filter(pk=pk, is_deleted=False)).exists():
            ride = rides.latest("date_added")

            serialized_data = ListRideSerializer(
                ride,
                context = {
                    "request" : request
                },
            ).data

            response_data = {
                "StatusCode" : 6000,
                "data" : serialized_data
            }
        else:
            response_data = {
                "StatusCode" : 6001,
                "data" : []
            }
    except Exception as e:
        transaction.rollback()
        errType = e.__class__.__name__
        errors = {
            errType: traceback.format_exc()
        }
        response_data = {
            "status": 0,
            "api": request.get_full_path(),
            "request": request.data,
            "message": str(e),
            "response": errors
        }

    return Response({'app_data': response_data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@group_required(['RiderProfile', 'DriverProfile'])
def update_ride_location(request, pk):
    try:
        serialized_data = UpdateRideLocationSerializer(data=request.data)

        if serialized_data.is_valid():
            latitude = request.data["latitude"]
            longitude = request.data["longitude"]

            ride = Ride.objects.get(pk=pk, is_deleted=False)

            ride_location = RideLocation.objects.create(
                ride=ride,
                latitude=latitude,
                longitude=longitude
            )
            
            # Send update to WebSocket consumers
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'ride_{pk}',
                {
                    'type': 'location_update',
                    'latitude': latitude,
                    'longitude': longitude,
                }
            )

            response_data = {
                "StatusCode" : 6000,
                "data" : {
                    "title" : "Success",
                    "ride_location_id":ride_location.id,
                    'message': 'Location updated successfully'
                }
            }
        else:
            response_data = {
                "StatusCode" : 6001,
                "data" : {
                    "title" : "Failed",
                    "message" : generate_serializer_errors(serialized_data._errors)
                }
            } 
    except Exception as e:
        transaction.rollback()
        errType = e.__class__.__name__
        errors = {
            errType: traceback.format_exc()
        }
        response_data = {
            "status": 0,
            "api": request.get_full_path(),
            "request": request.data,
            "message": str(e),
            "response": errors
        }

    return Response({'app_data': response_data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@group_required(['RiderProfile', 'DriverProfile'])
def track_ride_location(request, pk):
    try:
        if (ride_location := RideLocation.objects.filter(pk=pk, is_deleted=False)).exists():
            ride_location = ride_location.latest("date_added")

            serialized_data = RideLocationSerializer(
                ride_location,
                context = {
                    "request" : request
                },
            ).data

            response_data = {
                "StatusCode" : 6000,
                "data" : serialized_data
            }
        else:
            response_data = {
                "StatusCode" : 6001,
                "data" : {
                    "title" : "Failed",
                    "message" : "An error occured in tracking"
                }
            }
    except Exception as e:
        transaction.rollback()
        errType = e.__class__.__name__
        errors = {
            errType: traceback.format_exc()
        }
        response_data = {
            "status": 0,
            "api": request.get_full_path(),
            "request": request.data,
            "message": str(e),
            "response": errors
        }

    return Response({'app_data': response_data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@group_required(['DriverProfile'])
def ride_confirmation(request):
    try:
        transaction.set_autocommit(False)
        serialized_data = ConfirmRideSerializer(data=request.data)
        if serialized_data.is_valid():
            ride_id = request.data["ride_id"]
            is_confirm = request.data["is_confirm"]

            if (ride := Ride.objects.filter(pk=ride_id)).exists():
                ride = ride.latest("date_added")

                if is_confirm == "confirmed":
                    ride.status = 'accept'
                elif is_confirm == "rejected":
                    ride.status = 'cancelled'

                ride.save()
                transaction.commit()
                response_data = {
                    "StatusCode" : 6000,
                    "data" : {
                        "title": "Success",
                        "message" :"Ride confirmation updated successfully"
                    }
                }
            else:
                response_data = {
                    "StatusCode" : 6000,
                    "data" : {
                        "title" : "Failed",
                        "message" : "Ride not found"
                    }
                }
        else:
            response_data = {
                "StatusCode" : 6001,
                "data" : {
                    "title" : "Failed",
                    "message" : generate_serializer_errors(serialized_data._errors)
                }
            }
    except Exception as e:
        transaction.rollback()
        errType = e.__class__.__name__
        errors = {
            errType: traceback.format_exc()
        }
        response_data = {
            "status": 0,
            "api": request.get_full_path(),
            "request": request.data,
            "message": str(e),
            "response": errors
        }

    return Response({'app_data': response_data}, status=status.HTTP_200_OK)
