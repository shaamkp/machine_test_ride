from rest_framework import serializers

class LoginRiderSerializer(serializers.Serializer):
    name = serializers.CharField()
    password = serializers.CharField()


class LoginDriverSerializer(serializers.Serializer):
    name = serializers.CharField()
    password = serializers.CharField()



   