import pytest
from user.models import User
from rest_framework.test import APIClient
from customer.models import Customer
from dealership.models import Dealership
from supplier.models import Supplier
from ddf import G


@pytest.fixture
def user():
    return User.objects.create(username="test_user", password="test_password")


@pytest.fixture
def api_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def customer(user):
    user.user_role = "CUSTOMER"
    customer = G(Customer, user=user)
    return customer


@pytest.fixture
def dealership(user):
    user.user_role = "DEALERSHIP"
    dealership = G(Dealership, user=user)
    return dealership


@pytest.fixture
def supplier(user):
    user.user_role = "SUPPLIER"
    supplier = G(Supplier, user=user)
    return supplier
