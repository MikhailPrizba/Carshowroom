from customer.signals import buy_car_signal
from django.dispatch import receiver
from customer.models import CustomerOffer
from customer.tasks import buy_car


@receiver(buy_car_signal, sender=CustomerOffer)
def handle_dealership_car_sale(sender, instance, **kwargs):
    """
    Handle the dealership car sale when the buy_car_signal is received.

    This function is connected to the buy_car_signal signal and is triggered when
    a CustomerOffer instance is created. It initiates the buy_car task to process
    the car purchase asynchronously.
    """
    buy_car.delay(customer_offer_id=instance.id)
