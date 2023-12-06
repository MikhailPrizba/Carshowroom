from common.models import (
    CarInformationMixin,
    MainInformationMixin,
    UserInformationMixin,
    ModelManagerMixin,
    CustomQuerySetMixin,
)
from customer.models import Customer
from django.core.validators import MinValueValidator
from django.db import models
from user.models import User


class DealershipManager(ModelManagerMixin):
    """Manager for the Dealership class."""

    def create_instance(self, **kwargs) -> models.Model:
        """
        Create a new instance of Dealership and associate it with the user

        Args:
            **kwargs: Parameters for creating the instance  and associate it with the user.

        Returns:
            models.Model: Created instance.
        """
        user = User.objects.create_user(
            user_role=User.UserRoleChoices.DEALERSHIP, **kwargs.get("user")
        )
        kwargs["user"] = user
        instance = super().create_instance(**kwargs)
        return instance


class DealershipQuerySet(CustomQuerySetMixin):
    """QuerySet for the Dealership class."""

    pass


class DealershipCarManager(ModelManagerMixin):
    """Manager for the DealershipCar class."""

    def buy(self, instance, price):
        """
        Increase the quantity and update the balance when buying a car.

        Args:
            instance: DealershipCar instance.
            price: DealershipCar price.
        """
        instance.count += 1
        instance.dealership.balance -= price
        instance.dealership.save()
        instance.save()

    def sell(self, instance):
        """
        Decrease the quantity and update the balance when selling a car.

        Args:
            instance: DealershipCar instance.
        """
        instance.count -= 1
        instance.dealership.balance += instance.price
        instance.dealership.save()
        instance.save()


class DealershipCarQuerySet(CustomQuerySetMixin):
    """QuerySet for the DealershipCar class."""

    pass


class DealershipOfferManager(ModelManagerMixin):
    """Manager for the DealershipOffer class."""

    pass


class DealershipOfferQuerySet(CustomQuerySetMixin):
    """QuerySet for the DealershipOffer class."""

    pass


class Dealership(MainInformationMixin, UserInformationMixin):
    """Class representing a dealership."""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(
        default=0, max_digits=12, decimal_places=2, validators=[MinValueValidator(0.00)]
    )
    objects = DealershipManager().from_queryset(DealershipQuerySet)()


class DealershipCar(MainInformationMixin, CarInformationMixin):
    """Class representing a car available at the dealership."""

    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    price = models.DecimalField(
        default=0, max_digits=12, decimal_places=2, validators=[MinValueValidator(0.00)]
    )
    count = models.IntegerField(default=1, validators=[MinValueValidator(0)])
    objects = DealershipCarManager().from_queryset(DealershipCarQuerySet)()


class DealershipOffer(MainInformationMixin):
    """Class representing an offer from the dealership to a customer."""

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    max_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0.00)]
    )
    paid = models.BooleanField(default=False)
    objects = DealershipOfferManager().from_queryset(DealershipOfferQuerySet)()
