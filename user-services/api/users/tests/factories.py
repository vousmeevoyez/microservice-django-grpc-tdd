"""
    Test Factory using Factory boy
"""
from random import randint
from uuid import uuid4
from datetime import timedelta

from factory import (LazyFunction, DjangoModelFactory, Faker, fuzzy, SubFactory,
                     post_generation)

from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from api.users.models import (Device, Shop, Otp)
from api.users.choices import SUPPORTED_PLATFORMS, OTP_TYPES

User = get_user_model()


def get_phone_ext():
    phone_exts = ["62", "63", "64"]
    return phone_exts[randint(0, len(phone_exts) - 1)]


def get_device_id():
    return str(uuid4())


def get_otp_code():
    return make_password("1234")


def get_valid_until():
    return timezone.now() + timedelta(minutes=5)


class UserFactory(DjangoModelFactory):

    username = Faker("user_name")
    phone_ext = LazyFunction(get_phone_ext)
    phone_no = Faker("msisdn")
    email = Faker("email")
    first_name = Faker("first_name")
    middle_name = Faker("first_name")
    last_name = Faker("last_name")
    is_active = True

    @post_generation
    def password(self, create, extracted, **kwargs):
        if not (isinstance(self, dict)):
            self.set_password("password")

    class Meta:
        model = User


class DeviceFactory(DjangoModelFactory):

    user = SubFactory(UserFactory)
    platform = fuzzy.FuzzyChoice(SUPPORTED_PLATFORMS)
    device_id = LazyFunction(get_device_id)

    class Meta:
        model = Device


class ShopFactory(DjangoModelFactory):

    user = SubFactory(UserFactory)
    name = Faker("company")

    class Meta:
        model = Shop
