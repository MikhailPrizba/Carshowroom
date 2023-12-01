import pytest
from customer.models import CustomerOffer
from customer.signals import buy_car_signal
from ddf import G


@pytest.mark.django_db
class TestCustomerBuyCar:
    @pytest.fixture
    def mock_buy_car(self, mocker):
        return mocker.patch("customer.receivers.buy_car.delay")

    def test_buy_car_signal_handler(self, mock_buy_car):
        customer_offer = G(CustomerOffer)

        buy_car_signal.send(sender=CustomerOffer, instance=customer_offer)  # act

        mock_buy_car.assert_called_once_with(customer_offer_id=customer_offer.id)
