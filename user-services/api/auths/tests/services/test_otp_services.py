import pytest

from uuid import uuid4
from datetime import datetime, timedelta

from api.auths.models import Otp
from api.auths.services.otp import OtpService
from api.auths.exceptions import OtpNotFoundException, PendingOtpException


@pytest.mark.django_db
def test_generate_and_send_otp(user):
    OtpService(user).generate_and_send()
    # make sure otp object created
    otp = Otp.objects.get(user=user)
    assert otp.user == user
    assert otp.is_verified is False


@pytest.mark.django_db
def test_verify_otp_not_found():
    with pytest.raises(OtpNotFoundException):
        otp_id = str(uuid4())
        OtpService().verify(otp_id, "1234")


@pytest.mark.django_db
def test_verify_otp_expired(otp):
    with pytest.raises(OtpNotFoundException):
        # set otp so it already expired
        otp.valid_until = datetime.utcnow() - timedelta(minutes=5)
        otp.save()

        OtpService().verify(otp.id, "1234")


@pytest.mark.django_db
def test_verify_otp(otp):
    OtpService(otp_type=otp.otp_type).verify(otp.id, "1234")


@pytest.mark.django_db
def test_resend_otp(user):
    OtpService(user).resend()


@pytest.mark.django_db
def test_resend_otp_pending(otp):
    with pytest.raises(PendingOtpException):
        OtpService(otp.user).resend()
