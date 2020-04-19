"""
    Serializers
    _____________________
"""
from rest_framework.serializers import (Serializer, ModelSerializer, CharField,
                                        ChoiceField, RegexField)
from django.contrib.auth import get_user_model

from .choices import SUPPORTED_PLATFORMS
from .models import (Device, Shop)

User = get_user_model()


class UserRegistrationSerializer(ModelSerializer):

    shop_name = CharField()
    device_id = CharField()
    platform = ChoiceField(choices=SUPPORTED_PLATFORMS)

    class Meta:
        model = User
        fields = [
            "username", "phone_ext", "phone_no", "email", "first_name",
            "middle_name", "last_name", "password", "shop_name", "device_id",
            "platform"
        ]


class DeviceSerializer(ModelSerializer):

    class Meta:
        model = Device
        exclude = ["user"]


class ShopSerializer(ModelSerializer):

    class Meta:
        model = Shop
        exclude = ["user"]


class UserSerializer(ModelSerializer):

    shops = ShopSerializer(many=True)
    devices = DeviceSerializer(many=True)

    class Meta:
        model = User
        exclude = ["password", "groups", "user_permissions", "is_staff"]


class UserLoginSerializer(Serializer):

    username = CharField(required=True, allow_blank=False)
    password = CharField(required=True, allow_blank=False)


class VerifyUserSerializer(Serializer):

    otp_id = CharField(required=True, allow_blank=False)
    otp_code = RegexField(r"^[0-9]{4}$")
