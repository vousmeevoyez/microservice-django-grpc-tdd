import pytest
from django.contrib.auth.hashers import make_password

from api.ecommerces.models import Store, StorePlatform, Platform


@pytest.mark.django_db
def test_relation(store):
    assert store.name

    store_platforms = store.store_platforms.all()
    for store_platform in store_platforms:
        assert store_platform.platform.key
