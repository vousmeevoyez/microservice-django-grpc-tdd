import pytest
from faker import Faker

from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from api.users.serializers import *

User = get_user_model()


@pytest.mark.django_db
def test_user_registration_serializers():
    faker = Faker()
    request = {
        "username": faker.user_name(),
        "phone_ext": "62",
        "phone_no": faker.msisdn(),
        "email": faker.email(),
        "first_name": faker.first_name(),
        "middle_name": faker.first_name(),
        "last_name": faker.last_name(),
        "password": "password",
        "shop_name": "my-ol-shop",
        "device_id": "my-device-id",
        "platform": "MOBILE",
    }

    serializer = UserRegistrationSerializer(data=request)
    assert serializer.is_valid(raise_exception=True)


def test_verify_user_serializer_failed():
    request = {"otp_id": "some-otp-id", "otp_code": "00000000"}

    serializer = VerifyUserSerializer(data=request)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)

    request = {"otp_id": "some-otp-id", "otp_code": "1234"}
    serializer = VerifyUserSerializer(data=request)
    assert serializer.is_valid(raise_exception=True)


def test_update_password_serializer():
    request = {
        "current_password": "password",
        "new_password": "new_password",
        "confirm_password": "new_password",
    }

    serializer = UpdatePasswordSerializer(data=request)
    assert serializer.is_valid(raise_exception=True)

    request = {
        "current_password": "password",
        "new_password": "password",
        "confirm_password": "password",
    }

    with pytest.raises(ValidationError):
        serializer = UpdatePasswordSerializer(data=request)
        serializer.is_valid(raise_exception=True)


def test_update_msisdn_serializer():
    request = {"phone_ext": "62", "phone_no": "8121964314"}

    serializer = UpdateMsisdnSerializer(data=request)
    assert serializer.is_valid(raise_exception=True)

    request = {"phone_ext": "AA", "phone_no": "aaabbbbbbbbb"}

    with pytest.raises(ValidationError):
        serializer = UpdateMsisdnSerializer(data=request)
        serializer.is_valid(raise_exception=True)
