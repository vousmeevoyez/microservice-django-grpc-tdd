import pytest
from faker import Faker

from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from api.auths.serializers import (VerifyOtpSerializer)

User = get_user_model()


def test_verify_user_serializer_failed():
    request = {"otp_id": "some-otp-id", "otp_code": "00000000"}

    serializer = VerifyOtpSerializer(data=request)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)

    request = {"otp_id": "some-otp-id", "otp_code": "1234"}
    serializer = VerifyOtpSerializer(data=request)
    assert serializer.is_valid(raise_exception=True)
