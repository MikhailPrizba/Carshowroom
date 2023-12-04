from typing import Any
from common.models import (
    MainInformationMixin,
    UserInformationMixin,
    ModelManagerMixin,
    CarInformationMixin,
    CustomQuerySetMixin,
)
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from user.models import User
from customer.signals import buy_car_signal


class CustomerManager(ModelManagerMixin):
    def create_instance(self, **kwargs) -> models.Model:
        user = User.objects.create_user(
            user_role=User.UserRoleChoices.CUSTOMER, **kwargs.get("user")
        )
        kwargs["user"] = user
        instance = super().create_instance(**kwargs)
        return instance

    def buy(self, instance, price):
        instance.balance -= price
        instance.save()


class CustomerQuerySet(CustomQuerySetMixin):
    pass


class CustomerOfferManager(ModelManagerMixin):
    def create_instance(self, **kwargs):
        instance = super().create_instance(**kwargs)
        buy_car_signal.send(sender=CustomerOffer, instance=instance)
        return instance


class CustomerOfferQuerySet(CustomQuerySetMixin):
    pass


class Customer(MainInformationMixin, UserInformationMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(
        default=0, max_digits=12, decimal_places=2, validators=[MinValueValidator(0.00)]
    )
    objects = CustomerManager.from_queryset(CustomerOfferQuerySet)()


class CustomerOffer(CarInformationMixin, MainInformationMixin):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    max_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0.00)]
    )
    objects = CustomerOfferManager.from_queryset(CustomerOfferQuerySet)()
