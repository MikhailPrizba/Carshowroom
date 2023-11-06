from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries import fields
from django_enum import IntegerChoices, TextChoices


class MainInformation(models.Model):
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserInformation(models.Model):
    email = models.EmailField(max_length=254)
    email_confirm = models.BooleanField(default=False)
    phone_number = models.CharField(blank=True, validators=[
                                    RegexValidator(regex=r"^\+(?:[0-9] ?){6,14}[0-9]$")], max_length=12)
    location = fields.CountryField()

    class Meta:
        abstract = True


class Car(MainInformation):
    class CarType(TextChoices):
        SEDAN = "Sed", _("Sedan")
        COUPE = "Cou", _("Coupe")
        MINIVAN = "Van", _("Minivan")
        PICKUP = "Pic", _("Pickup")
        HATCHBACK = "Hat", _("Hatchback")

    mark = models.CharField(max_length=7)
    model = models.CharField(max_length=7, default='Unknown')
    car_type = models.CharField(
        max_length=3, choices=CarType.choices, default=CarType.SEDAN)
    color = models.CharField(blank=True, max_length=10, default='Unknown')
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    class UserLevel(IntegerChoices):
        UNKNOWN = 0
        ADMIN = 1
        SUPPLIER = 2
        DEALERSHIP = 3
        CUSTOMER = 4

    user_level = models.IntegerField(
        choices=UserLevel.choices, default=UserLevel.UNKNOWN)

    def __str__(self):
        return self.username
