import pytest
from django.urls import reverse
from rest_framework import status
from dealership.models import Dealership
from ddf import G


@pytest.mark.django_db
class TestDealershipViews:
    def test_get_dealership(self, api_client):
        # Arrange
        G(Dealership)
        url = reverse("dealership-list")

        # Act
        response = api_client.get(url)

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_create_dealership(self, api_client):
        # Arrange
        dealership_data = {
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
        url = reverse("dealership-list")

        # Act
        response = api_client.post(url, dealership_data, format="json")

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert Dealership.objects.filter(is_active=True).exists()

    def test_delete_dealership(self, api_client):
        # Arrange
        dealership = G(Dealership)
        delete_url = reverse("dealership-detail", args=[dealership.id])

        # Act
        response = api_client.delete(delete_url)

        # Assert
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Dealership.objects.filter(id=dealership.id, is_active=False).exists()
