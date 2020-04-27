"""
    Serializers
    _____________________
"""
from rest_framework.serializers import (
    Serializer,
    CharField,
    RegexField,
    ValidationError,
)


class LoginSerializer(Serializer):

    username = CharField(required=True, allow_blank=False)
    password = CharField(required=True, allow_blank=False)


class ForgotPasswordSerializer(Serializer):

    otp_id = CharField(required=True, allow_blank=False)
    otp_code = RegexField(r"^[0-9]{4}$")
    password = CharField(required=True, allow_blank=False)
    confirm_password = CharField(required=True, allow_blank=False)

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise ValidationError("mismatch password and confirm password")
        return data


class VerifyOtpSerializer(Serializer):

    otp_id = CharField(required=True, allow_blank=False)
    otp_code = RegexField(r"^[0-9]{4}$")
