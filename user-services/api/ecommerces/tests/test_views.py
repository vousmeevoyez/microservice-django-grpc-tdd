"""
    API Test
"""
from uuid import uuid4
import pytest
from unittest.mock import patch
from django.urls import reverse


@pytest.mark.django_db
def test_crud_platforms_api(api_client, user):
    url = reverse("platform-list")
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data

    url = reverse("platform-list")
    payload = {"key": "INSTAGRAM", "description": "instagram"}
    response = api_client.post(url, payload, format="json")
    assert response.status_code == 201
    assert response.data
    platform_id = response.data["id"]

    url = reverse("platform-detail", args=(platform_id,))
    response = api_client.get(url, None, format="json")
    assert response.status_code == 200
    assert response.data
