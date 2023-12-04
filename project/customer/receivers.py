from customer.signals import buy_car_signal
from django.dispatch import receiver
from customer.models import CustomerOffer
from customer.tasks import buy_car


@receiver(buy_car_signal, sender=CustomerOffer)
def handle_dealership_car_sale(sender, instance, **kwargs):
    buy_car.delay(customer_offer_id=instance.id)
