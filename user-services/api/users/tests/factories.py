"""
    Test Factory using Factory boy
"""
from random import randint
from uuid import uuid4
from datetime import timedelta

from factory import (LazyFunction, DjangoModelFactory, Faker, fuzzy, SubFactory,
                     post_generation)

from django.contrib.auth import get_user_model

from api.users.models import (Device, Shop)
from api.users.choices import SUPPORTED_PLATFORMS

User = get_user_model()


def get_phone_ext():
    phone_exts = ["62", "63", "64"]
    return phone_exts[randint(0, len(phone_exts) - 1)]


def get_device_id():
    return str(uuid4())


class UserFactory(DjangoModelFactory):

    phone_ext = LazyFunction(get_phone_ext)
    phone_no = Faker("msisdn")
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
