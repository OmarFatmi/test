from django.test import TestCase
# tests/auth.spec.py

import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from monapp.models import Organisation

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

def test_register_user(api_client):
    # Test registering a user without organization details
    url = reverse('register_user')  # Adjust the view name as per your URL configuration
    data = {
        'firstName': 'John',
        'lastName': 'Doe',
        'email': 'john.doe@example.com',
        'password': 'securepassword'
    }

    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED

    # Verify default organization name and user details in the response
    assert "organisation" in response.data
    assert response.data["organisation"]["name"] == "John's Organisation"
    assert "user" in response.data
    assert response.data["user"]["firstName"] == 'John'
    assert response.data["user"]["email"] == 'john.doe@example.com'
    assert "accessToken" in response.data

def test_login_user(api_client):
    # Test logging in a registered user
    url = reverse('login_user')  # Adjust the view name as per your URL configuration
    data = {
        'email': 'john.doe@example.com',
        'password': 'securepassword'
    }

    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
  
