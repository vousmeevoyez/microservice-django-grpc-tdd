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
