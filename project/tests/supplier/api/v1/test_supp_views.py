import pytest
from django.urls import reverse
from rest_framework import status
from supplier.models import Supplier, SupplierCar
from ddf import G


@pytest.mark.django_db
class TestSupplierViews:
    @pytest.fixture
    def supplier_data(self):
        data = {
            "user": {
                "username": "supplier",
                "email": "supplier@email.com",
                "password": "supplierpassword",
            },
            "phone_number": "+1234567890",
            "balance": 100,
            "foundation_year": 2000,
            "location": "AF",
            "email_confirm": True,
            "is_active": True,
        }
        return data

    @pytest.fixture
    def url(self):
        return reverse("supplier-list")

    @pytest.fixture
    def url_detail(self, supplier):
        return reverse("supplier-detail", args=[supplier.id])

    def test_get_supplier(self, supplier_client, url):
        # Arrange
        # Act
        response = supplier_client.get(url)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_create_supplier(self, supplier_client, url, supplier_data):
        # Arrange
        # Act
        response = supplier_client.post(url, supplier_data, format="json")

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert Supplier.objects.filter(is_active=True).exists()

    def test_delete_supplier(self, supplier_client, supplier, url_detail):
        # Arrange
        # Act
        response = supplier_client.delete(url_detail)

        # Assert
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Supplier.objects.filter(id=supplier.id, is_active=True).exists()


@pytest.mark.django_db
class TestSupplierCar:
    @pytest.fixture
    def supplier_car(self, supplier):
        return G(SupplierCar, supplier=supplier)

    @pytest.fixture
    def url(self):
        return reverse("supplier_car-list")

    @pytest.fixture
    def url_detail(self, supplier_car):
        return reverse("supplier_car-detail", args=[supplier_car.id])

    def test_get_supplier_car(self, supplier_client, supplier_car, url):
        # Arrange
        # Act
        response = supplier_client.get(url)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_create_supplier_car(self, supplier_client, url):
        # Arrange
        supplier_car_data = {
            "mark": "Toyota",
            "model": "Camry",
            "price": 25000.00,
            "count": 2,
        }
        # Act
        response = supplier_client.post(url, supplier_car_data, format="json")

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert SupplierCar.objects.filter(is_active=True).exists()

    def test_delete_supplier_car(self, supplier_client, supplier_car, url_detail):
        # Arrange
        # Act
        response = supplier_client.delete(url_detail)

        # Assert
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not SupplierCar.objects.filter(
            id=supplier_car.id, is_active=True
        ).exists()
