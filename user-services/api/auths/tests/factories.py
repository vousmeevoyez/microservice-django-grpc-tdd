"""
    Test Factory using Factory boy
"""
from random import randint
from uuid import uuid4
from datetime import timedelta

from factory import (LazyFunction, DjangoModelFactory, fuzzy, SubFactory, Trait)

from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from api.auths.models import (Otp)
from api.auths.choices import OTP_TYPES

from api.users.tests.factories import UserFactory

User = get_user_model()


def get_otp_code():
    return make_password("1234")


def get_valid_until():
    return timezone.now() + timedelta(minutes=5)


class OtpFactory(DjangoModelFactory):

    user = SubFactory(UserFactory)
    code = LazyFunction(get_otp_code)
    valid_until = LazyFunction(get_valid_until)

    class Meta:
        model = Otp

    class Params:
        is_register = Trait(otp_type=OTP_TYPES[0][0])
        is_forgot_password = Trait(otp_type=OTP_TYPES[1])
