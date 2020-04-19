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
from api.users.models.otp import Otp


@pytest.mark.django_db
def test_user_models():
    fake = Faker()
    User.objects.create(username=fake.first_name(),
                        email=fake.email(),
                        phone_ext=fake.country_calling_code()[:3],
                        phone_no=fake.phone_number()[:16],
                        first_name=fake.first_name(),
                        last_name=fake.last_name())
    # make sure use create
    assert len(User.objects.all()) > 0


@pytest.mark.django_db
def test_user_relation(shop, device):
    assert Shop.objects.get(user=User.objects.get(username=shop.user))
    assert Device.objects.get(user=User.objects.get(username=device.user))


@pytest.mark.django_db
def test_otp(user):
    otp = Otp(user=user, otp_type="REGISTER")
    otp.generate()
    # make sure right information is generate
    record = Otp.objects.get(id=otp.id)
    assert record.otp_type
    assert record.code
    assert record.is_verified is False
