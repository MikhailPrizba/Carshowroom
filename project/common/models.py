from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries import fields
from django_enum import TextChoices
import uuid


class MainInformationMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserInformationMixin(models.Model):
    email_confirm = models.BooleanField(default=False)
    phone_number = models.CharField(
        blank=True,
        validators=[RegexValidator(regex=r"^\+(?:[0-9] ?){6,14}[0-9]$")],
        max_length=12,
    )
    location = fields.CountryField()

    class Meta:
        abstract = True


class CarInformationMixin(models.Model):
    class CarType(TextChoices):
        SEDAN = "Sed", _("Sedan")
        COUPE = "Cou", _("Coupe")
        MINIVAN = "Van", _("Minivan")
        PICKUP = "Pic", _("Pickup")
        HATCHBACK = "Hat", _("Hatchback")

    mark = models.CharField(max_length=7)
    model = models.CharField(max_length=7, default="Unknown")
    car_type = models.CharField(
        max_length=3, choices=CarType.choices, default=CarType.SEDAN
    )
    color = models.CharField(blank=True, max_length=10, default="Unknown")
    description = models.TextField(blank=True)

    class Meta:
        abstract = True


class ModelManagerMixin(models.Manager):
    """
    A mixin for managing generic models.

    Attributes:
    - None

    Methods:
    - create_instance(username: str, email: str, password: str, **kwargs) -> ModelInstance:
        Creates a new instance with the given user credentials and additional keyword arguments.
        Returns the created instance.

    - update_instance(id: int, **kwargs) -> ModelInstance:
        Updates the instance with the specified ID using the provided keyword arguments.
        Returns the updated instance.
    """

    def create_instance(self, **kwargs) -> models.Model:
        return self.create(**kwargs)

    def update_instance(self, id: int, **kwargs) -> models.Model:
        self.filter(id=id).update(**kwargs)
        return self.get(id=id)
