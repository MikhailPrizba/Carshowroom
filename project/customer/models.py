from common.models import MainInformationMixin, UserInformationMixin, ModelManagerMixin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from user.models import User


class CustomerManager(ModelManagerMixin):
    def create_instance(self, **kwargs) -> models.Model:
        user = User.objects.create_user(**kwargs.get("user"))
        kwargs["user"] = user
        instance = super().create_instance(**kwargs)
        return instance


class Customer(MainInformationMixin, UserInformationMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(
        default=0, max_digits=12, decimal_places=2, validators=[MinValueValidator(0.00)]
    )
    objects = CustomerManager()
