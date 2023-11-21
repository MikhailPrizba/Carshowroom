import pytest
from user.models import User
from rest_framework.test import APIClient


@pytest.fixture
def user():
    return User.objects.create(username="test_user", password="test_password")


@pytest.fixture
def api_client():
    client = APIClient()
    return client
