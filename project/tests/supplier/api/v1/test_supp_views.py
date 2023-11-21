import pytest
from django.urls import reverse
from rest_framework import status
from supplier.models import Supplier
from ddf import G


@pytest.mark.django_db
class TestSupplierViews:
    def test_get_supplier(self, api_client):
        # Arrange
        G(Supplier)
        url = reverse("supplier-list")

        # Act
        response = api_client.get(url)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_create_supplier(self, api_client):
        # Arrange
        supplier_data = {
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
        url = reverse("supplier-list")

        # Act
        response = api_client.post(url, supplier_data, format="json")

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert Supplier.objects.filter(is_active=True).exists()

    def test_delete_supplier(self, api_client):
        # Arrange
        supplier = G(Supplier)
        delete_url = reverse("supplier-detail", args=[supplier.id])

        # Act
        response = api_client.delete(delete_url)

        # Assert
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Supplier.objects.filter(id=supplier.id, is_active=False).exists()
