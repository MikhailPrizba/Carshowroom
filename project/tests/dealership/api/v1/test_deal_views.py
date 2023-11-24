import pytest
from django.urls import reverse
from rest_framework import status
from dealership.models import Dealership, DealershipCar
from ddf import G


@pytest.mark.django_db
class TestDealershipViews:
    @pytest.fixture
    def dealership_data(self):
        data = {
            "user": {
                "username": "dealership",
                "email": "dealership@email.com",
                "password": "dealershippassword",
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
        return reverse("dealership-list")

    @pytest.fixture
    def url_detail(self, dealership):
        return reverse("dealership-detail", args=[dealership.id])

    def test_get_dealership(self, dealership_client, url):
        # Arrange
        # Act
        response = dealership_client.get(url)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_create_dealership(self, dealership_client, dealership_data, url):
        # Arrange
        # Act
        response = dealership_client.post(url, dealership_data, format="json")

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert Dealership.objects.filter(is_active=True).exists()

    def test_delete_dealership(self, dealership_client, dealership, url_detail):
        # Arrange
        # Act
        response = dealership_client.delete(url_detail)

        # Assert
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Dealership.objects.filter(id=dealership.id, is_active=True).exists()


@pytest.mark.django_db
class TestDealershipCar:
    @pytest.fixture
    def dealership_car(self, dealership):
        return G(DealershipCar, dealership=dealership)

    @pytest.fixture
    def url(self):
        return reverse("dealership_car-list")

    @pytest.fixture
    def url_detail(self, dealership_car):
        return reverse("dealership_car-detail", args=[dealership_car.id])

    def test_get_dealership_car(self, dealership_client, dealership_car, url):
        # Arrange
        # Act
        response = dealership_client.get(url)
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_create_dealership_car(self, dealership_client, url):
        # Arrange
        dealership_car_data = {
            "mark": "Toyota",
            "model": "Camry",
            "price": 25000.00,
            "count": 2,
        }

        # Act
        response = dealership_client.post(url, dealership_car_data, format="json")

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert DealershipCar.objects.filter(is_active=True).exists()

    def test_delete_dealership_car(self, dealership_client, dealership_car, url_detail):
        # Arrange
        # Act
        response = dealership_client.delete(url_detail)

        # Assert
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not DealershipCar.objects.filter(
            id=dealership_car.id, is_active=True
        ).exists()
