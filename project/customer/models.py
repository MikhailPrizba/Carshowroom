from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from common.models import MainInformationMixin, UserInformationMixin
from user.models import User





class Customer(MainInformationMixin, UserInformationMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2, validators=[MinValueValidator(0.00)])

