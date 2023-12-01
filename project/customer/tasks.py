from celery import shared_task
from dealership.models import Dealership, DealershipCar
from customer.models import Customer, CustomerOffer
from django.db import transaction


@shared_task
def buy_car(customer_offer_id):
    dealership__active_cars = DealershipCar.objects.get_is_active().filter(
        dealership__is_active=True
    )
    customer_offer = CustomerOffer.objects.get(id=customer_offer_id)

    dealership_cars = dealership__active_cars.filter(
        mark=customer_offer.mark,
        model=customer_offer.model,
        car_type=customer_offer.car_type,
        color=customer_offer.color,
        price__lte=customer_offer.max_price,
        count__gte=1,
    )
    if not dealership_cars:
        return
    dealership_car = dealership_cars.order_by("price").first()

    if customer_offer.customer.balance >= dealership_car.price:
        with transaction.atomic():
            DealershipCar.objects.sell(dealership_car)
            Customer.objects.buy(customer_offer.customer, dealership_car.price)
