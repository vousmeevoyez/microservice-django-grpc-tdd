import pytest
from faker import Faker

from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from api.auths.serializers import (
    LoginSerializer,
    ForgotPasswordSerializer,
    VerifyOtpSerializer,
)

User = get_user_model()


def test_login_serializer():
    request = {"username": "some-username", "password": "password"}

    serializer = LoginSerializer(data=request)
    assert serializer.is_valid(raise_exception=True)

    request = {"username": "", "password": ""}
    with pytest.raises(ValidationError):
        serializer = LoginSerializer(data=request)
        serializer.is_valid(raise_exception=True)


def test_forgot_password_serializer():
    request = {
        "otp_id": "otp_id",
        "otp_code": "1234",
        "password": "password",
        "confirm_password": "password",
    }

    serializer = ForgotPasswordSerializer(data=request)
    assert serializer.is_valid(raise_exception=True)

    request = {
        "otp_id": "",
        "otp_code": "adasdasads",
        "password": "",
        "confirm_password": "",
    }

    with pytest.raises(ValidationError):
        serializer = ForgotPasswordSerializer(data=request)
        assert serializer.is_valid(raise_exception=True)


def test_verify_user_serializer():
    request = {"otp_id": "some-otp-id", "otp_code": "00000000"}

    serializer = VerifyOtpSerializer(data=request)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)

    request = {"otp_id": "some-otp-id", "otp_code": "1234"}
    serializer = VerifyOtpSerializer(data=request)
    assert serializer.is_valid(raise_exception=True)
