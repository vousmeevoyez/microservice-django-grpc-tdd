import uuid
import pytest
from unittest.mock import patch

from api.auths.services.auth import *
from api.auths.exceptions import (InactiveUserException,
                                  InvalidCredentialsException,
                                  OldPasswordException)


@pytest.mark.django_db
@patch("api.auths.services.auth.CLIENT")
def test_jwt_generate(mock_kong, user, create_jwt_credential_response):
    """ test generate jwt for user """
    mock_kong.create_jwt_credential.return_value =\
        create_jwt_credential_response

    jwt = JWTToken(user.id).generate()
    assert jwt


@pytest.mark.django_db
@patch("api.auths.services.auth.CLIENT")
def test_jwt_remove(mock_kong, user):
    """ test remove jwt """
    mock_kong.delete_jwt_credential.return_value = 204
    JWTToken(user.id).remove()


@pytest.mark.django_db
@patch("api.auths.services.auth.JWTToken")
def test_login_success(mock_jwt, user):
    """ test login using valid user and valid credentials """
    mock_jwt.return_value.generate.return_value = b'some-valid-jwt'
    username = user.username
    response = login(username, "password")
    assert response["access_token"] == "some-valid-jwt"


@pytest.mark.django_db
def test_login_failed_inactive(user):
    """ test login using valid user and valid credentials but inactive"""
    username = user.username
    # deactivate
    user.is_active = False
    user.save()

    with pytest.raises(InactiveUserException):
        login(username, "password")


@pytest.mark.django_db
def test_login_failed_invalid_credentials():
    """ test login using invalid user and invalid credentials"""
    with pytest.raises(InvalidCredentialsException):
        login("randomusername", "randompassword")


@pytest.mark.django_db
@patch("api.auths.services.auth.JWTToken")
def test_logout_success(mock_jwt, user):
    """ test logout """
    mock_jwt.return_value.remove.return_value = True
    logout(user.id)


@pytest.mark.django_db
@patch("api.auths.services.auth.JWTToken")
def test_logout_success(mock_jwt, user):
    """ test logout """
    mock_jwt.return_value.remove.return_value = True
    logout(user.id)


@pytest.mark.django_db
@patch("api.auths.services.otp.OtpService")
def test_request_reset_password_success(mock_otp, user):
    """ test logout """
    mock_otp.return_value.generate_and_send.return_value = str(uuid.uuid4())
    assert request_reset_password(user.id)


@pytest.mark.django_db
@patch("api.auths.services.otp.OtpService")
def test_reset_password_success(mock_otp, reset_password_otp):
    """ test reset password """
    mock_otp.return_value.verify.return_value = reset_password_otp
    reset_password(reset_password_otp.id, "1234", "password")


@pytest.mark.django_db
def test_update_password_success(user):
    """ test update password """
    update_password(user, "newpassword")


@pytest.mark.django_db
def test_update_password_failed(user):
    """ test update password failed new password same as old one"""
    with pytest.raises(OldPasswordException):
        update_password(user, "password")
