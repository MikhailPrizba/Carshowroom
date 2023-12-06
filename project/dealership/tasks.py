from project.celery import app
from dealership.models import DealershipCar
from supplier.models import SupplierCar
from django.db import transaction


@app.task
def buy_car():
    """
    Task to handle the process of buying a car from a supplier for a dealership.

    This task retrieves active cars from both the dealership and the supplier,
    matches them based on certain criteria, and conducts the transaction.

    Note:
        This task assumes that the models involved have appropriate methods
        like 'get_is_active()', 'sell()', and 'buy()' defined.

    """
    # Retrieve active dealership cars
    dealership_cars = DealershipCar.objects.get_is_active().filter(
        dealership__is_active=True
    )

    supplier_active_cars = SupplierCar.objects.get_is_active()

    for dealership_car in dealership_cars.iterator():
        supplier_cars = supplier_active_cars.filter(
            mark=dealership_car.mark,
            model=dealership_car.model,
            car_type=dealership_car.car_type,
            color=dealership_car.color,
            price__lte=dealership_car.price,
            count__gte=1,
        )

        if not supplier_cars:
            continue

        supplier_car = supplier_cars.order_by("price").first()

        if dealership_car.dealership.balance >= supplier_car.price:
            with transaction.atomic():
                SupplierCar.objects.sell(supplier_car)
                DealershipCar.objects.buy(dealership_car, supplier_car.price)
