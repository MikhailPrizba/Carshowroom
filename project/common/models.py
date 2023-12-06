from django.core.validators import RegexValidator
from django.db import models
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _
from django_countries import fields
from django_enum import TextChoices
import uuid


class MainInformationMixin(models.Model):
    """
    Main Information Mixin for common fields in models.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserInformationMixin(models.Model):
    """
    User Information Mixin for additional user-related fields.
    """

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
    """
    Car Information Mixin for common car-related fields in models.
    """

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


class CustomQuerySetMixin(models.QuerySet):
    """
    Custom QuerySet Mixin with additional methods.
    """

    def get_is_active(self):
        """
        Return QuerySet filtering active instances.
        """
        return self.filter(is_active=True)


class ModelManagerMixin(models.Manager):
    """
    A mixin for managing generic models.

    Attributes:
    - None

    Methods:
    - create_instance(**kwargs) -> models.Model:
        Creates a new instance with the given keyword arguments.
        Returns the created instance.

    - update_instance(id: int, **kwargs) -> models.Model:
        Updates the instance with the specified ID using the provided keyword arguments.
        Returns the updated instance.

    - soft_delete(instance: models.Model):
        Soft deletes the given instance by setting 'is_active' to False.
    """

    def create_instance(self, **kwargs) -> models.Model:
        """
        Create a new instance with the given keyword arguments.

        Args:
        - kwargs: Additional keyword arguments.

        Returns:
        - models.Model: The created instance.
        """
        return self.create(**kwargs)

    def update_instance(self, id: int, **kwargs) -> models.Model:
        """
        Update the instance with the specified ID using the provided keyword arguments.

        Args:
        - id: The ID of the instance to be updated.
        - kwargs: Keyword arguments for updating the instance.

        Returns:
        - models.Model: The updated instance.
        """
        self.filter(id=id).update(**kwargs)
        return self.get(id=id)

    def soft_delete(self, instance: models.Model):
        """
        Soft delete the given instance by setting 'is_active' to False.

        Args:
        - instance: The instance to be soft deleted.
        """
        instance.is_active = False
        instance.save()
