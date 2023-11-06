from django.db import models
from django_enum import TextChoices
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    class UserLevel(TextChoices):
        UNKNOWN = 'UNKNOWN'
        ADMIN = 'ADMIN'
        SUPPLIER = 'SUPPLIER'
        DEALERSHIP = 'DEALERSHIP'
        CUSTOMER = 'CUSTOMER'

    user_level = models.IntegerField(
        choices=UserLevel.choices, default=UserLevel.UNKNOWN)

    def __str__(self):
        return self.username