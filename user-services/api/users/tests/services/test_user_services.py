import pytest
from uuid import uuid4
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.db import DatabaseError

from api.users.services.users import *
from api.users.exceptions import (FailedRegistrationException,
                                  UserNotFoundException, OldMsisdnException)
from api.auths.exceptions import InvalidOtpException


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
def test_update_phone_no(user):
    update_phone_no(user, "62", "8777177317")


@pytest.mark.django_db
def test_update_phone_no_old_msisdn(user):
    with pytest.raises(OldMsisdnException):
        update_phone_no(user, user.phone_ext, user.phone_no)
