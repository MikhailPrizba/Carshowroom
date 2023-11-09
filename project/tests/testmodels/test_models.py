import pytest
from supplier.models import Supplier, SupplierCar, SupplierOffer
from dealership.models import Dealership
from ddf import G

@pytest.mark.django_db
class TestSupplier:
    
    def test_supplier_creation(self):
        supplier = Supplier.objects.create_instance(username='supplier', email='supplier@email.com', password='supplierpassword', phone_number='+1234567890', foundation_year = 2000, balance = 100)
        assert supplier.user.username == 'supplier'
        assert supplier.user.email == 'supplier@email.com'
        assert supplier.phone_number == '+1234567890'
        assert supplier.foundation_year == 2000
        assert supplier.balance == 100

    def test_supplier_update(self):
        G(Supplier)
        supplier = Supplier.objects.update_instance(id = 1,phone_number='+9876543210')
        assert supplier.phone_number == '+9876543210'


@pytest.mark.django_db
class TestSupplierCar:

    def test_supplier_car_creation(self):
        supplier = G(Supplier)
        supplier_car = SupplierCar.objects.create_instance(supplier=supplier, mark = 'Toyota', model='Camry', price=25000.00, count=2)
        
        assert supplier_car.supplier == supplier
        assert supplier_car.model == 'Camry'
        assert supplier_car.price == 25000.00
        assert supplier_car.count == 2

    def test_supplier_car_update(self):
        G(SupplierCar)
        supplier_car = SupplierCar.objects.update_instance(id =1,model='Civic', price=22000.00, count=1)
        assert supplier_car.price == 22000.00
        assert supplier_car.count == 1


@pytest.mark.django_db
class TestSupplierOffer:

    def test_supplier_offer_creation(self):
        supplier = G(Supplier)
        dealership = G(Dealership)
        supplier_offer = SupplierOffer.objects.create_instance(supplier=supplier, dealership=dealership, max_price=30000.00, paid=False)
        assert supplier_offer.supplier == supplier
        assert supplier_offer.dealership == dealership
        assert supplier_offer.max_price == 30000.00
        assert not supplier_offer.paid

    def test_supplier_offer_update(self):
        G(SupplierOffer)
        supplier_offer = SupplierOffer.objects.update_instance(id =1, max_price=28000.00, paid=True)
        assert supplier_offer.max_price == 28000.00
        assert supplier_offer.paid
