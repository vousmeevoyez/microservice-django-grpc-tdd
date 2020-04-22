import pytest
from unittest.mock import patch

from api.auths.services.auth import (login, logout, JWTToken)
from api.auths.exceptions import (InactiveUserException,
                                  InvalidCredentialsException)


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
