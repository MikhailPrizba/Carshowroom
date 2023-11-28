import datetime

from common.models import (
    CarInformationMixin,
    MainInformationMixin,
    UserInformationMixin,
    ModelManagerMixin,
    CustomQuerySetMixin,
)
from dealership.models import Dealership
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from user.models import User


class SupplierManager(ModelManagerMixin):
    def create_instance(self, **kwargs) -> models.Model:
        user = User.objects.create_user(
            user_role=User.UserRoleChoices.SUPPLIER, **kwargs.get("user")
        )
        kwargs["user"] = user
        instance = super().create_instance(**kwargs)
        return instance


class SupplierQuerySet(CustomQuerySetMixin):
    pass


class SupplierCarManager(ModelManagerMixin):
    def sell(self, instance):
        instance.count -= 1
        instance.save()


class SupplierCarQuerySet(CustomQuerySetMixin):
    pass


class SupplierOfferManager(ModelManagerMixin):
    pass


class SupplierOfferQuerySet(CustomQuerySetMixin):
    pass


class Supplier(MainInformationMixin, UserInformationMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    foundation_year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(datetime.date.today().year),
        ]
    )
    balance = models.DecimalField(
        default=0, max_digits=15, decimal_places=2, validators=[MinValueValidator(0.00)]
    )
    objects = SupplierManager().from_queryset(SupplierQuerySet)()


class SupplierCar(MainInformationMixin, CarInformationMixin):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    price = models.DecimalField(
        max_digits=12, decimal_places=2, validators=[MinValueValidator(0.00)]
    )
    count = models.IntegerField(default=1, validators=[MinValueValidator(0)])
    objects = SupplierCarManager().from_queryset(SupplierCarQuerySet)()


class SupplierOffer(MainInformationMixin):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    max_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0.00)]
    )
    paid = models.BooleanField(default=False)
    objects = SupplierOfferManager().from_queryset(SupplierOfferQuerySet)()
