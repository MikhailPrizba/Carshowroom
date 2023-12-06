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
    """Manager for the Customer model."""

    def create_instance(self, **kwargs) -> models.Model:
        """
        Create a new instance of the Customer model and associate it with the user.

        Args:
            **kwargs: Parameters for creating the instance.

        Returns:
            models.Model: Created instance.
        """
        user = User.objects.create_user(
            user_role=User.UserRoleChoices.CUSTOMER, **kwargs.get("user")
        )
        kwargs["user"] = user
        instance = super().create_instance(**kwargs)
        return instance

    def buy(self, instance, price):
        """
        Handle the buying action for a customer.

        Args:
            instance: Customer instance.
            price: Price of the item being bought.
        """
        instance.balance -= price
        instance.save()


class CustomerQuerySet(CustomQuerySetMixin):
    """Custom QuerySet for the Customer model."""

    pass


class CustomerOfferManager(ModelManagerMixin):
    """Manager for the CustomerOffer model."""

    def create_instance(self, **kwargs):
        """
        Create a new instance of the CustomerOffer model and send signals.

        Args:
            **kwargs: Parameters for creating the instance.

        Returns:
            models.Model: Created instance.
        """
        instance = super().create_instance(**kwargs)
        buy_car_signal.send(sender=CustomerOffer, instance=instance)
        return instance


class CustomerOfferQuerySet(CustomQuerySetMixin):
    """Custom QuerySet for the CustomerOffer model."""

    pass


class Customer(MainInformationMixin, UserInformationMixin):
    """Model representing a customer."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(
        default=0, max_digits=12, decimal_places=2, validators=[MinValueValidator(0.00)]
    )
    objects = CustomerManager.from_queryset(CustomerOfferQuerySet)()


class CustomerOffer(CarInformationMixin, MainInformationMixin):
    """Model representing a customer's offer on a car."""

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    max_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0.00)]
    )
    objects = CustomerOfferManager.from_queryset(CustomerOfferQuerySet)()
