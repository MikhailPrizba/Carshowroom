import pytest
from dealership.models import Dealership, DealershipCar
from customer.models import Customer, CustomerOffer
from customer.tasks import buy_car
from ddf import G


@pytest.mark.django_db
class TestCustomerBuyCar:
    def test_buy(self):
        # ARRANGE
        dealership = G(Dealership, balance=500)
        dealership_car_1, dealership_car_2, dealership_car_3 = G(
            DealershipCar, dealership=dealership, count=3, price=250, mark="mark", n=3
        )
        customer = G(Customer, balance=500)

        customer_offer = G(CustomerOffer, max_price=300, mark="mark", customer=customer)
        # ACT

        buy_car(customer_offer.id)
        # ASSERT
        updated_dealership_balance = Dealership.objects.get(id=dealership.id).balance
        updated_customer_balance = Customer.objects.get(id=customer.id).balance
        updated_dealership_car_1 = DealershipCar.objects.get(
            id=dealership_car_1.id
        ).count
        updated_dealership_car_2 = DealershipCar.objects.get(
            id=dealership_car_2.id
        ).count
        updated_dealership_car_3 = DealershipCar.objects.get(
            id=dealership_car_3.id
        ).count

        assert updated_dealership_car_1 == 2
        assert updated_dealership_car_2 == 3
        assert updated_dealership_car_3 == 3
        assert updated_dealership_balance == 750
        assert updated_customer_balance == 250
