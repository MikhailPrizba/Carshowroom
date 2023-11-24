import pytest
from user.models import User
from rest_framework.test import APIClient
from customer.models import Customer
from dealership.models import Dealership
from supplier.models import Supplier
from ddf import G


def api_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def customer():
    user = G(User, user_role=User.UserRoleChoices.CUSTOMER)
    instance = G(Customer, user=user)
    return instance


@pytest.fixture
def customer_client(customer):
    return api_client(customer.user)


@pytest.fixture
def dealership():
    user = G(User, user_role=User.UserRoleChoices.DEALERSHIP)
    instance = G(Dealership, user=user)
    return instance


@pytest.fixture
def dealership_client(dealership):
    return api_client(dealership.user)


@pytest.fixture
def supplier():
    user = G(User, user_role=User.UserRoleChoices.SUPPLIER)
    instance = G(Supplier, user=user)
    return instance


@pytest.fixture
def supplier_client(supplier):
    return api_client(supplier.user)
