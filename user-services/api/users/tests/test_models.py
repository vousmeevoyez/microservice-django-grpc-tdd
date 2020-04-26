"""
    Test Models
    _____________
"""
from datetime import datetime
import pytest
from faker import Faker

from api.users.models.user import User
from api.users.models.device import Device
from api.users.models.shop import Shop


@pytest.mark.django_db
def test_user_models(user):
    assert user.profile
    assert len(User.objects.all()) > 0


@pytest.mark.django_db
def test_user_relation(shop, device):
    assert Shop.objects.get(user=User.objects.get(username=shop.user))
    assert Device.objects.get(user=User.objects.get(username=device.user))
