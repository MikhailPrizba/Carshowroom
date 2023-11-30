import pytest
from dealership.models import Dealership, DealershipCar
from supplier.models import SupplierCar
from dealership.tasks import buy_car
from ddf import G


@pytest.mark.django_db
class TestDealershipBuyCar:
    def test_buy(self):
        # ARRANGE
        dealership = G(Dealership, balance=500)
        dealership_car_1, dealership_car_2, dealership_car_3 = G(
            DealershipCar, dealership=dealership, count=3, price=250, mark="mark", n=3
        )

        G(SupplierCar, price=200, mark="mark", count=4)
        G(SupplierCar, price=240, mark="mark", count=4)
        # ACT

        buy_car()
        # ASSERT
        updated_dealership = Dealership.objects.get(id=dealership.id).balance
        updated_dealership_car_1 = DealershipCar.objects.get(
            id=dealership_car_1.id
        ).count
        updated_dealership_car_2 = DealershipCar.objects.get(
            id=dealership_car_2.id
        ).count
        updated_dealership_car_3 = DealershipCar.objects.get(
            id=dealership_car_3.id
        ).count
        assert updated_dealership_car_1 == 4
        assert updated_dealership_car_2 == 4
        assert updated_dealership_car_3 == 3
        assert updated_dealership == 100
