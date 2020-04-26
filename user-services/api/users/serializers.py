"""
    Serializers
    _____________________
"""
from rest_framework.serializers import (Serializer, ModelSerializer, CharField,
                                        ChoiceField, RegexField)
from django.contrib.auth import get_user_model

from api.users.choices import SUPPORTED_PLATFORMS
from api.users.models import (Device, Shop, Profile)

User = get_user_model()


class ProfileSerializer(ModelSerializer):

    class Meta:
        model = Profile
        exclude = ["is_active", "user"]


class UserRegistrationSerializer(ModelSerializer):

    shop_name = CharField()
    device_id = CharField()
    platform = ChoiceField(choices=SUPPORTED_PLATFORMS)

    class Meta:
        model = User
        fields = [
            "phone_ext", "phone_no", "shop_name", "device_id", "platform",
            "password"
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
    profile = ProfileSerializer()

    class Meta:
        model = User
        exclude = ["password", "groups", "user_permissions", "is_staff"]


class UserLoginSerializer(Serializer):

    username = CharField(required=True, allow_blank=False)
    password = CharField(required=True, allow_blank=False)


class VerifyUserSerializer(Serializer):

    otp_id = CharField(required=True, allow_blank=False)
    otp_code = RegexField(r"^[0-9]{4}$")
