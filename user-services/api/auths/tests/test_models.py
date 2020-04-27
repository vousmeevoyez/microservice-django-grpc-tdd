import pytest
from django.contrib.auth.hashers import make_password

from api.auths.models import Otp


@pytest.mark.django_db
def test_generate_code():
    otp = Otp()
    generated_code = otp._generate_code()
    assert len(generated_code) == 4

    generated_code = otp._generate_code(no_of_digits=6)
    assert len(generated_code) == 6


@pytest.mark.django_db
def test_is_available(otp):
    hashed_otp_code = make_password("1235")
    is_available = otp._is_available(hashed_otp_code)
    assert is_available


@pytest.mark.django_db
def test_generate(user):
    otp = Otp(user=user)
    assert otp.generate()
