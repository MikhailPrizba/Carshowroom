import pytest
from customer.models import Customer
from ddf import G


@pytest.mark.django_db
class TestCustomerModel:
    def test_customer_creation(self):
        # ARRANGE
        customer_data = {
            "username": "customer",
            "email": "customer@email.com",
            "password": "customerpassword",
            "phone_number": "+1234567890",
            "balance": 100,
        }

        # ACT
        customer = Customer.objects.create_instance(**customer_data)

        # ASSERT
        assert customer.user.username == customer_data["username"]
        assert customer.user.email == customer_data["email"]
        assert customer.phone_number == customer_data["phone_number"]
        assert customer.balance == customer_data["balance"]

    def test_customer_update(self):
        # ARRANGE
        customer = G(Customer)

        # ACT
        updated_customer = Customer.objects.update_instance(
            id=customer.id, phone_number="+9876543210"
        )

        # ASSERT
        assert updated_customer.phone_number == "+9876543210"
