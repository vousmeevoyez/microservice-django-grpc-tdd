"""
    API Test
"""
import pytest
from unittest.mock import patch
from django.urls import reverse


@pytest.mark.django_db
def test_resend_otp_api(api_client, user):
    url = reverse("otp-resend", kwargs={"user_id": user.id})
    response = api_client.post(url)
    assert response.status_code == 200


@pytest.mark.django_db
@patch("requests.request")
def test_login_api_success(mock_request, api_client, user,
                           create_jwt_credential_response):

    mock_request.return_value.status_code.return_value == 201
    mock_request.return_value.json.return_value =\
        create_jwt_credential_response

    url = reverse("user-login")
    auth_payload = {"username": user.username, "password": "password"}
    response = api_client.post(url, auth_payload, format="json")
    assert response.status_code == 200
    assert response.data["access_token"]


@pytest.mark.django_db
def test_login_api_failed(api_client, user):
    url = reverse("user-login")
    auth_payload = {"username": "random-username", "password": "password"}
    response = api_client.post(url, auth_payload, format="json")
    assert response.status_code == 401


@pytest.mark.django_db
@patch("requests.request")
def test_logout_success(mock_request, api_client, user):

    mock_request.return_value.status_code.return_value == 204

    url = reverse("user-logout")
    response = api_client.post(url,
                               None,
                               format="json",
                               headers={"HTTP_X_CONSUMER_CUSTOM_ID": user.id})
    assert response.status_code == 204
