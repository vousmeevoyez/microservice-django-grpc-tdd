"""
    Serializers
    _____________________
"""
from rest_framework.fields import CurrentUserDefault
from rest_framework.serializers import (Serializer, ModelSerializer, CharField,
                                        ChoiceField, RegexField, EmailField,
                                        ValidationError)
from django.contrib.auth import get_user_model

from api.users.choices import SUPPORTED_PLATFORMS
from api.users.models import (Device, Profile)

User = get_user_model()


class ProfileSerializer(ModelSerializer):

    class Meta:
        model = Profile
        exclude = ["is_active", "user"]


class UserRegistrationSerializer(ModelSerializer):

    device_id = CharField()
    platform = ChoiceField(choices=SUPPORTED_PLATFORMS)

    class Meta:
        model = User
        fields = ["phone_ext", "phone_no", "device_id", "platform", "password"]


class DeviceSerializer(ModelSerializer):

    class Meta:
        model = Device
        exclude = ["user"]


class UserSerializer(ModelSerializer):

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


class UpdatePasswordSerializer(Serializer):
    current_password = CharField(required=True, allow_blank=False)
    new_password = CharField(required=True, allow_blank=False)
    confirm_password = CharField(required=True, allow_blank=False)

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise ValidationError("MISMATCH_NEW_CONFIRM_PASSWORD")

        if data["new_password"] == data["current_password"]:
            raise ValidationError("SAME_PASSWORD")
        return data


class UpdateMsisdnSerializer(Serializer):
    phone_ext = RegexField(r"^[0-9]{2}$")  # only allow 0-9 and must be 2 digit
    phone_no = RegexField(
        r"^[0-9]{8,12}$")  # only allow 0-9 and must be 2 digit
