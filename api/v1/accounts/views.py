import traceback

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from django.db import transaction

from general.functions import generate_serializer_errors, loginUser
from general.encryptions import decrypt
from accounts.models import *
from api.v1.accounts.serializers import *
from general.decorators import group_required

from django.contrib.auth.models import Group, User


@api_view(['POST'])
@permission_classes([AllowAny,])
def login_rider(request):
    try:
        transaction.set_autocommit(False)
        serialized_data = LoginRiderSerializer(data=request.data)
        if serialized_data.is_valid():
            name = request.data["name"]
            password = request.data["password"]

            if (rider_profile := RiderProfile.objects.filter(name=name)).exists():
                rider_profile = rider_profile.latest('date_added')

                decrypted_password = decrypt(rider_profile.password)
                if decrypted_password == password:
                    access = loginUser(request, rider_profile.user)

                    transaction.commit()
                    response_data = {
                        "StatusCode" : 6000,
                        "data" : {
                            "title" : "Success",
                            "access" : access
                        }
                    }
                else:
                    response_data = {
                        "StatusCode" : 6001,
                        "data" : {
                            "title" : "Failed",
                            "message" : "Incorrect"
                        }
                    }
            else:
                response_data = {
                    "StatusCode" : 6001,
                    "data" : {
                        "title" : "Failed",
                        "message" : "Chief profile does not exists"
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

    return Response({'dev_data': response_data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_driver(request):
    try:
        print("in view")
        transaction.set_autocommit(False)
        serialized_data = LoginDriverSerializer(data=request.data)
        if serialized_data.is_valid():
            name = request.data["name"]
            password = request.data["password"]

            if (driver_profile := DriverProfile.objects.filter(name=name)).exists():
                driver_profile = driver_profile.latest('date_added')

                decrypted_password = decrypt(driver_profile.password)
                if decrypted_password == password:
                    access = loginUser(request, driver_profile.user)

                    transaction.commit()
                    response_data = {
                        "StatusCode" : 6000,
                        "data" : {
                            "title" : "Success",
                            "access" : access
                        }
                    }
                else:
                    response_data = {
                        "StatusCode" : 6001,
                        "data" : {
                            "title" : "Failed",
                            "message" : "Incorrect"
                        }
                    }
            else:
                response_data = {
                    "StatusCode" : 6001,
                    "data" : {
                        "title" : "Failed",
                        "message" : "Chief profile does not exists"
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

    return Response({'dev_data': response_data}, status=status.HTTP_200_OK)




