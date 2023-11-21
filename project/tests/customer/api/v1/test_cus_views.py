import pytest
from django.urls import reverse
from rest_framework import status
from customer.models import Customer, CustomerOffer
from ddf import G


@pytest.mark.django_db
class TestCustomerViews:
    def test_get_customer(self, api_client):
        # Arrange
        G(Customer)
        url = reverse("customer-list")

        # Act
        response = api_client.get(url)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_create_customer(self, api_client):
        # Arrange
        customer_data = {
            "user": {
                "username": "customer",
                "email": "customer@email.com",
                "password": "customerpassword",
            },
            "phone_number": "+1234567890",
            "balance": 100,
            "location": "AF",
            "email_confirm": True,
            "is_active": True,
        }
        url = reverse("customer-list")

        # Act
        response = api_client.post(url, customer_data, format="json")

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert Customer.objects.filter(is_active=True).exists()

    def test_delete_customer(self, api_client):
        # Arrange
        customer = G(Customer)
        delete_url = reverse("customer-detail", args=[customer.id])

        # Act
        response = api_client.delete(delete_url)

        # Assert
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Customer.objects.filter(id=customer.id, is_active=False).exists()


@pytest.mark.django_db
class TestCustomerOffer:
    def test_get_customeroffer(self, api_client, customer):
        # Arrange

        G(CustomerOffer, customer=customer)
        url = reverse("customer_offer-list")

        # Act
        response = api_client.get(url)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_create_offer(self, api_client, customer):
        # Arrange
        customer_offer_data = {
            "mark": "Toyota",
            "model": "Camry",
            "max_price": 25000.00,
            "count": 2,
        }
        url = reverse("customer_offer-list")

        # Act
        response = api_client.post(url, customer_offer_data, format="json")

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert CustomerOffer.objects.filter(is_active=True).exists()

    def test_delete_offer(self, api_client, customer):
        # Arrange
        customer_offer = G(CustomerOffer, customer=customer)
        delete_url = reverse("customer_offer-detail", args=[customer_offer.id])

        # Act
        response = api_client.delete(delete_url)

        # Assert
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert CustomerOffer.objects.filter(
            id=customer_offer.id, is_active=False
        ).exists()
