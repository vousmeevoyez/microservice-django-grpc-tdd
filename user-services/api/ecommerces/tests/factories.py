"""
    Test Factory using Factory boy
"""
from faker import Faker

from factory import (
    LazyFunction,
    DjangoModelFactory,
    fuzzy,
    SubFactory,
    Trait,
    Iterator,
    RelatedFactoryList,
)

from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from api.ecommerces.models import Store, StorePlatform, Platform

from api.users.tests.factories import UserFactory

User = get_user_model()

PLATFORMS = Platform.objects.all()


def generate_store_name():
    faker = Faker()
    return "shop " + faker.company()


class StoreFactory(DjangoModelFactory):

    user = SubFactory(UserFactory)
    name = LazyFunction(generate_store_name)
    platform = RelatedFactoryList(
        "api.ecommerces.tests.factories.StorePlatformFactory", "store", size=2
    )

    class Meta:
        model = Store


class StorePlatformFactory(DjangoModelFactory):

    store = SubFactory(StoreFactory)
    platform = Iterator(PLATFORMS)

    class Meta:
        model = StorePlatform
