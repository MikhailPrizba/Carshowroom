from common.models import (
    CarInformationMixin,
    MainInformationMixin,
    UserInformationMixin,
    ModelManagerMixin,
)
from customer.models import Customer
from django.core.validators import MinValueValidator
from django.db import models
from user.models import User


class DealershipManager(ModelManagerMixin):
    def create_instance(
        self, username: str, email: str, password: str, **kwargs
    ) -> models.Model:
        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        kwargs["user"] = user
        instance = super().create_instance(**kwargs)
        return instance


class DealershipCarManager(ModelManagerMixin):
    pass


class DealershipOfferManager(ModelManagerMixin):
    pass


class Dealership(MainInformationMixin, UserInformationMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(
        default=0, max_digits=12, decimal_places=2, validators=[MinValueValidator(0.00)]
    )
    objects = DealershipManager()


class DealershipCar(MainInformationMixin, CarInformationMixin):
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    price = models.DecimalField(
        default=0, max_digits=12, decimal_places=2, validators=[MinValueValidator(0.00)]
    )
    count = models.IntegerField(default=1, validators=[MinValueValidator(0)])
    objects = DealershipCarManager()


class DealershipOffer(MainInformationMixin):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    max_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0.00)]
    )
    paid = models.BooleanField(default=False)
    objects = DealershipOfferManager()
