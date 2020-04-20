import pytest
from uuid import uuid4
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.db import DatabaseError

from api.users.services.users import (create_user, verify_user, resend_user_otp)
from api.users.exceptions import (FailedRegistrationException,
                                  InvalidOtpException, OtpNotFoundException,
                                  UserNotFoundException)


@pytest.mark.django_db
def test_create_user(registration_payload):
    user, otp_id = create_user(**registration_payload)
    assert user
    assert otp_id


@pytest.mark.django_db
@patch("api.users.services.users.User")
def test_create_user_failed(mock_user, registration_payload):
    mock_user.objects.create.side_effect = DatabaseError
    with pytest.raises(FailedRegistrationException):
        create_user(**registration_payload)
    # make sure no user is created
    User = get_user_model()
    assert len(User.objects.all()) == 0


@pytest.mark.django_db
def test_verify_user(otp):
    verify_user(otp.id, "1234")
    # make sure user is activated
    assert otp.user.is_active


@pytest.mark.django_db
def test_verify_user_wrong_otp(otp):
    with pytest.raises(InvalidOtpException):
        verify_user(otp.id, "123123123")


@pytest.mark.django_db
def test_resend_user_otp_not_found():
    with pytest.raises(UserNotFoundException):
        resend_user_otp(str(uuid4()))


@pytest.mark.django_db
def test_resend_user_otp(user):
    otp_id = resend_user_otp(user.id)
    assert otp_id
