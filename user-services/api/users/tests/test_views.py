"""
    API Test
"""
import pytest
from unittest.mock import patch
from django.urls import reverse


@pytest.mark.django_db
def test_user_registration_api(api_client, registration_payload):
    url = reverse("user-registration")
    response = api_client.post(url, registration_payload, format="json")
    assert response.status_code == 200
    assert response.data
    # make sure its contain otp
    assert response.data["otp"]


@pytest.mark.django_db
def test_user_verification_api(api_client, otp):
    url = reverse("user-verification")
    payload = {"otp_id": otp.id, "otp_code": "1234"}
    response = api_client.post(url, payload, format="json")
    assert response.status_code == 204


@pytest.mark.django_db
def test_user_profile_api(api_client, user):
    url = reverse("user-profile")
    headers = {"HTTP_X_CONSUMER_CUSTOM_ID": user.id}
    response = api_client.get(url, None, format="json", headers=headers)
    assert response.status_code == 200
    assert response.data["profile"]
    assert response.data["devices"] == []


@pytest.mark.django_db
def test_update_user_password_api(api_client, user):
    url = reverse("user-password")
    headers = {"HTTP_X_CONSUMER_CUSTOM_ID": user.id}
    payload = {
        "current_password": "password",
        "new_password": "newpassword",
        "confirm_password": "newpassword",
    }
    response = api_client.put(url, payload, format="json", headers=headers)
    assert response.status_code == 204


@pytest.mark.django_db
def test_update_user_phone_api(api_client, user):
    url = reverse("user-phone")
    headers = {"HTTP_X_CONSUMER_CUSTOM_ID": user.id}
    payload = {"phone_ext": "62", "phone_no": "8121111111"}
    response = api_client.put(url, payload, format="json", headers=headers)
    assert response.status_code == 204
