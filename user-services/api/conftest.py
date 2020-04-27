import pytest
from django.core.management import call_command
from factory import build

from api.users.tests.factories import (UserFactory, DeviceFactory)
from api.ecommerces.tests.factories import (StoreFactory)
from api.auths.tests.factories import OtpFactory


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'api/ecommerces/fixtures/platform.json')


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def otp():
    return OtpFactory(is_register=True)


@pytest.fixture
def reset_password_otp():
    return OtpFactory(is_register=False, is_reset_password=True)


@pytest.fixture
def store():
    return StoreFactory()


@pytest.fixture
def registration_payload():
    user_payload = build(dict, FACTORY_CLASS=UserFactory)
    user_payload.pop("is_active")
    # we do it like this because otherwise there's error
    user_payload["password"] = "password"

    #shop_payload = build(dict, FACTORY_CLASS=ShopFactory)
    #shop_payload.pop("user")
    #shop_payload["shop_name"] = shop_payload["name"]
    #shop_payload.pop("name")

    device_payload = build(dict, FACTORY_CLASS=DeviceFactory)
    device_payload.pop("user")

    device_payload["platform"] = device_payload["platform"][0]

    payload = {
        **user_payload,
        **device_payload,
        #**shop_payload,
        # "user_type": "MERCHANT"
    }
    return payload


@pytest.fixture
def create_consumer_response():
    response = {
        "id": "ec1a1f6f-2aa4-4e58-93ff-b56368f19b27",
        "created_at": 1422386534,
        "username": "",
        "custom_id": "some-user-id",
        "tags": []
    }
    return response


@pytest.fixture
def create_jwt_credential_response():
    response = {
        "consumer_id": "7bce93e1-0a90-489c-c887-d385545f8f4b",
        "created_at": 1442426001000,
        "id": "bcbfb45d-e391-42bf-c2ed-94e32946753a",
        "key": "a36c3049b36249a3c9f8891cb127243c",
        "secret": "e71829c351aa4242c2719cbfbe671c09"
    }
    return response
