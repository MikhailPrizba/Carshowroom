import pytest
from customer.models import CustomerOffer
from customer.signals import buy_car_signal
from ddf import G


@pytest.fixture
def mock_buy_car(mocker):
    return mocker.patch("customer.signals.buy_car.delay")


@pytest.mark.django_db
def test_buy_car_signal_handler(mock_buy_car):
    # ARRANGE
    customer_offer = G(CustomerOffer)

    # ACT
    buy_car_signal.send(sender=CustomerOffer, instance=customer_offer)

    # ASSERT
    mock_buy_car.assert_called_once_with(customer_offer_id=customer_offer.id)
