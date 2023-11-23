import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from customer.models import Customer, CustomerOffer
from ddf import G


@pytest.mark.django_db
class TestCustomerViews:
    @pytest.fixture
    def customer_data(self):
        data = {
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
        return data

    @pytest.fixture
    def url(self):
        return reverse("customer-list")

    @pytest.fixture
    def url_detail(self, customer):
        return reverse("customer-detail", args=[customer.id])

    def test_get_customer(self, customer_client: APIClient, url: str):
        # Arrange

        # Act
        response = customer_client.get(url)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_create_customer(
        self, customer_client: APIClient, customer_data: dict, url: str
    ):
        # Arrange
        # Act
        response = customer_client.post(url, customer_data, format="json")

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert Customer.objects.filter(is_active=True).exists()

    def test_delete_customer(
        self, customer_client: APIClient, customer: Customer, url_detail: str
    ):
        # Arrange
        # Act
        response = customer_client.delete(url_detail)

        # Assert
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Customer.objects.filter(id=customer.id, is_active=True).exists()


@pytest.mark.django_db
class TestCustomerOffer:
    @pytest.fixture
    def customer_offer_data(self):
        data = {
            "mark": "Toyota",
            "model": "Camry",
            "max_price": 25000.00,
            "count": 2,
        }
        return data

    @pytest.fixture
    def customer_offer(self, customer):
        return G(CustomerOffer, customer=customer)

    @pytest.fixture
    def url(self):
        return reverse("customer_offer-list")

    @pytest.fixture
    def url_detail(self, customer_offer):
        return reverse("customer_offer-detail", args=[customer_offer.id])

    def test_get_customer_offer(
        self,
        customer_client: APIClient,
        url: str,
        customer_offer: CustomerOffer,
    ):
        # Arrange
        # Act
        response = customer_client.get(url)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_create_offer(
        self, customer_client: APIClient, customer_offer_data: dict, url: str
    ):
        # Arrange
        # Act
        response = customer_client.post(url, customer_offer_data, format="json")

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert CustomerOffer.objects.filter(is_active=True).exists()

    def test_delete_offer(
        self,
        customer_client: APIClient,
        url_detail: str,
        customer_offer: CustomerOffer,
    ):
        # Arrange
        # Act
        response = customer_client.delete(url_detail)
        # Assert
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not CustomerOffer.objects.filter(
            id=customer_offer.id, is_active=True
        ).exists()
