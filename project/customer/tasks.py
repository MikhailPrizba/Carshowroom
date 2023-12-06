from dealership.models import DealershipCar
from customer.models import Customer, CustomerOffer
from django.db import transaction
from project.celery import app


@app.task
def buy_car(customer_offer_id):
    """
    Process the purchase of a car based on a customer's offer.

    This Celery task is responsible for handling the purchase of a car based on a
    customer's offer. It retrieves active dealership cars that match the criteria
    specified in the customer's offer and proceeds with the purchase if a suitable
    car is found and the customer has sufficient balance.

    Parameters:
        customer_offer_id (int): The ID of the CustomerOffer instance.

    Note:
        This task is expected to be called asynchronously using Celery.
    """
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
