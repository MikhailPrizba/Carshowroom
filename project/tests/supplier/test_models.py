import pytest
from supplier.models import Supplier, SupplierCar, SupplierOffer
from dealership.models import Dealership
from ddf import G


@pytest.mark.django_db
class TestSupplierModel:
    def test_supplier_creation(self):
        # ARRANGE
        supplier_data = {
            "user": {
                "username": "supplier",
                "email": "supplier@email.com",
                "password": "supplierpassword",
            },
            "phone_number": "+1234567890",
            "foundation_year": 2000,
            "balance": 100,
        }

        # ACT
        supplier = Supplier.objects.create_instance(**supplier_data)

        # ASSERT
        assert supplier.user.username == supplier_data["user"]["username"]
        assert supplier.user.email == supplier_data["user"]["email"]
        assert supplier.phone_number == supplier_data["phone_number"]
        assert supplier.foundation_year == supplier_data["foundation_year"]
        assert supplier.balance == supplier_data["balance"]

    def test_supplier_update(self):
        # ARRANGE
        supplier = G(Supplier)

        # ACT
        updated_supplier = Supplier.objects.update_instance(
            id=supplier.id, phone_number="+9876543210"
        )

        # ASSERT
        assert updated_supplier.phone_number == "+9876543210"


@pytest.mark.django_db
class TestSupplierCarModel:
    def test_supplier_car_creation(self):
        # ARRANGE
        supplier = G(Supplier)

        # ACT
        supplier_car = SupplierCar.objects.create_instance(
            supplier=supplier, mark="Toyota", model="Camry", price=25000.00, count=2
        )

        # ASSERT
        assert supplier_car.supplier == supplier
        assert supplier_car.model == "Camry"
        assert supplier_car.price == 25000.00
        assert supplier_car.count == 2

    def test_supplier_car_update(self):
        # ARRANGE
        supplier_car = G(SupplierCar)

        # ACT
        updated_supplier_car = SupplierCar.objects.update_instance(
            id=supplier_car.id, model="Civic", price=22000.00, count=1
        )

        # ASSERT
        assert updated_supplier_car.price == 22000.00
        assert updated_supplier_car.count == 1


@pytest.mark.django_db
class TestSupplierOfferModel:
    def test_supplier_offer_creation(self):
        # ARRANGE
        supplier = G(Supplier)
        dealership = G(Dealership)
        supplier_offer_data = {
            "supplier": supplier,
            "dealership": dealership,
            "max_price": 30000.00,
            "paid": False,
        }

        # ACT
        supplier_offer = SupplierOffer.objects.create_instance(**supplier_offer_data)

        # ASSERT
        assert supplier_offer.supplier == supplier
        assert supplier_offer.dealership == dealership
        assert supplier_offer.max_price == 30000.00
        assert not supplier_offer.paid

    def test_supplier_offer_update(self):
        # ARRANGE
        supplier_offer = G(SupplierOffer)

        # ACT
        updated_supplier_offer = SupplierOffer.objects.update_instance(
            id=supplier_offer.id, max_price=28000.00, paid=True
        )

        # ASSERT
        assert updated_supplier_offer.max_price == 28000.00
        assert updated_supplier_offer.paid
