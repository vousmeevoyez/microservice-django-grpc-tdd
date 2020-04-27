"""
    Test Models
    _____________
"""
from datetime import datetime
import pytest
from faker import Faker

from api.users.models.user import User
from api.users.models.device import Device


@pytest.mark.django_db
def test_user_models(user):
    assert user.profile
    assert len(User.objects.all()) > 0
