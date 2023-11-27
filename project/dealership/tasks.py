import datetime
from celery import shared_task
from dealership.models import Dealership, DealershipCar
from supplier.models import Supplier, SupplierCar, SupplierOffer
from django.db import connection
from django.db import transaction


@shared_task
def buy_car():
    dealership_cars = (
        DealershipCar.objects.get_is_active()
        .filter(dealership__is_active=True)
        .select_related("dealership")
    )
    supplier_active_cars = SupplierCar.objects.get_is_active()
    for dealership_car in dealership_cars:
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
    print(f"Количество выполненных запросов: {len(connection.queries)}")
