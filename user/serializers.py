from rest_framework import serializers
from .models import UserEntity


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, required=False)
    name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(max_length=255, required=False)

    def create(self, validated_data):
        return UserEntity(**validated_data)
