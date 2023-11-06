import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from common.models import CarInformationMixin, MainInformationMixin, UserInformationMixin
from dealership.models import Dealership
from user.models import User

class Supplier(MainInformationMixin, UserInformationMixin):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    foundation_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(datetime.date.today().year)]
    )
    balance = models.DecimalField(default=0, max_digits=15, decimal_places=2, validators=[MinValueValidator(0.00)])



class SupplierCar(MainInformationMixin, CarInformationMixin):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0.00)])
    count = models.IntegerField(default=1, validators=[MinValueValidator(0)])



class SupplierOffer(MainInformationMixin):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    max_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.00)])
    paid = models.BooleanField(default=False)