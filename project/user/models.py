from django.contrib.auth.models import AbstractUser
from django.db import models
from django_enum import TextChoices
import uuid

# Create your models here.


class User(AbstractUser):
    class UserRoleChoices(TextChoices):
        UNKNOWN = "UNKNOWN"
        ADMIN = "ADMIN"
        SUPPLIER = "SUPPLIER"
        DEALERSHIP = "DEALERSHIP"
        CUSTOMER = "CUSTOMER"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_role = models.TextField(
        choices=UserRoleChoices.choices, default=UserRoleChoices.UNKNOWN
    )

    def __str__(self):
        return self.username
