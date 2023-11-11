from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries import fields
from django_enum import TextChoices
from user.models import User


class MainInformationMixin(models.Model):
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
    def create_instance(self, username, email, password, **kwargs):
        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        kwargs["user"] = user
        return self.create(**kwargs)

    def update_instance(self, id, **kwargs):
        self.filter(id=id).update(**kwargs)
        return self.get(id=id)


class ModelCarManagerMixin(models.Manager):
    def create_instance(self, **kwargs):
        return self.create(**kwargs)

    def update_instance(self, id, **kwargs):
        self.filter(id=id).update(**kwargs)
        return self.get(id=id)


class ModelOfferManagerMixin(models.Manager):
    def create_instance(self, **kwargs):
        return self.create(**kwargs)

    def update_instance(self, id, **kwargs):
        self.filter(id=id).update(**kwargs)
        return self.get(id=id)
