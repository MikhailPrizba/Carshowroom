import pytest
from customer.models import Customer
from dealership.models import Dealership, DealershipCar, DealershipOffer
from ddf import G


@pytest.mark.django_db
class TestDealershipModel:
    def test_dealership_creation(self):
        # ARRANGE
        dealership_data = {
            "user": {
                "username": "dealership",
                "email": "dealership@email.com",
                "password": "dealershippassword",
            },
            "phone_number": "+1234567890",
            "balance": 100,
        }

        # ACT
        dealership = Dealership.objects.create_instance(**dealership_data)

        # ASSERT
        assert dealership.user.username == dealership_data["user"]["username"]
        assert dealership.user.email == dealership_data["user"]["email"]
        assert dealership.phone_number == dealership_data["phone_number"]
        assert dealership.balance == dealership_data["balance"]

    def test_dealership_update(self):
        # ARRANGE
        dealership = G(Dealership)

        # ACT
        updated_dealership = Dealership.objects.update_instance(
            id=dealership.id, phone_number="+9876543210"
        )

        # ASSERT
        assert updated_dealership.phone_number == "+9876543210"


@pytest.mark.django_db
class TestDealershipCarModel:
    def test_dealership_car_creation(self):
        # ARRANGE
        dealership = G(Dealership)

        # ACT
        dealership_car = DealershipCar.objects.create_instance(
            dealership=dealership, mark="Toyota", model="Camry", price=25000.00, count=2
        )

        # ASSERT
        assert dealership_car.dealership == dealership
        assert dealership_car.model == "Camry"
        assert dealership_car.price == 25000.00
        assert dealership_car.count == 2

    def test_dealership_car_update(self):
        # ARRANGE
        dealership_car = G(DealershipCar)

        # ACT
        updated_dealership_car = DealershipCar.objects.update_instance(
            id=dealership_car.id, model="Civic", price=22000.00, count=1
        )

        # ASSERT
        assert updated_dealership_car.price == 22000.00
        assert updated_dealership_car.count == 1


@pytest.mark.django_db
class TestDealershipOfferModel:
    def test_dealership_offer_creation(self):
        # ARRANGE
        customer = G(Customer)
        dealership = G(Dealership)
        dealership_offer_data = {
            "dealership": dealership,
            "customer": customer,
            "max_price": 30000.00,
            "paid": False,
        }

        # ACT
        dealership_offer = DealershipOffer.objects.create_instance(
            **dealership_offer_data
        )

        # ASSERT
        assert dealership_offer.dealership == dealership
        assert dealership_offer.customer == customer
        assert dealership_offer.max_price == 30000.00
        assert not dealership_offer.paid

    def test_dealership_offer_update(self):
        # ARRANGE
        dealership_offer = G(DealershipOffer)

        # ACT
        updated_dealership_offer = DealershipOffer.objects.update_instance(
            id=dealership_offer.id, max_price=28000.00, paid=True
        )

        # ASSERT
        assert updated_dealership_offer.max_price == 28000.00
        assert updated_dealership_offer.paid
