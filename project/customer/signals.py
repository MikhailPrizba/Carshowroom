from django.dispatch import Signal
from django.dispatch import receiver
from django.db.models.signals import post_save
from customer.models import CustomerOffer
from customer.tasks import buy_car

buy_car_signal = Signal()


@receiver(buy_car_signal, sender=CustomerOffer)
def handle_dealership_car_sale(sender, instance, **kwargs):
    buy_car.delay(customer_offer_id=instance.id)
