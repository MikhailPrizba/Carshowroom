import datetime

from common.models import (
    CarInformationMixin,
    MainInformationMixin,
    UserInformationMixin,
)
from dealership.models import Dealership
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from user.models import User


class SupplierManager(models.Manager):
    def create_instance(
        self, username: str, email: str, password: str, **kwargs
    ) -> "Supplier":
        """
        Create a new Supplier instance with a related User.

        Parameters:
        - username (str): The username for the User.
        - email (str): The email for the User.
        - password (str): The password for the User.
        - **kwargs: Additional fields for the Supplier model.

        Returns:
        - Supplier: The created Supplier instance.
        """
        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        kwargs["user"] = user
        return self.create(**kwargs)

    def update_instance(self, id: int, **kwargs) -> "Supplier":
        """
        Update a Supplier instance.

        Parameters:
        - id (int): The ID of the Supplier instance to be updated.
        - **kwargs: Fields to be updated.

        Returns:
        - Supplier: The updated Supplier instance.
        """
        self.filter(id=id).update(**kwargs)
        return self.get(id=id)


class SupplierCarManager(models.Manager):
    def create_instance(self, **kwargs) -> "SupplierCar":
        """
        Create a new SupplierCar instance.

        Parameters:
        - **kwargs: Fields for the SupplierCar model.

        Returns:
        - SupplierCar: The created SupplierCar instance.
        """
        return self.create(**kwargs)

    def update_instance(self, id: int, **kwargs) -> "SupplierCar":
        """
        Update a SupplierCar instance.

        Parameters:
        - id (int): The ID of the SupplierCar instance to be updated.
        - **kwargs: Fields to be updated.

        Returns:
        - SupplierCar: The updated SupplierCar instance.
        """
        self.filter(id=id).update(**kwargs)
        return self.get(id=id)


class SupplierOfferManager(models.Manager):
    def create_instance(self, **kwargs) -> "SupplierOffer":
        """
        Create a new SupplierOffer instance.

        Parameters:
        - **kwargs: Fields for the SupplierOffer model.

        Returns:
        - SupplierOffer: The created SupplierOffer instance.
        """
        return self.create(**kwargs)

    def update_instance(self, id: int, **kwargs) -> "SupplierOffer":
        """
        Update a SupplierOffer instance.

        Parameters:
        - id (int): The ID of the SupplierOffer instance to be updated.
        - **kwargs: Fields to be updated.

        Returns:
        - SupplierOffer: The updated SupplierOffer instance.
        """
        self.filter(id=id).update(**kwargs)
        return self.get(id=id)


class Supplier(MainInformationMixin, UserInformationMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    foundation_year = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(datetime.date.today().year),
        ]
    )
    balance = models.DecimalField(
        default=0, max_digits=15, decimal_places=2, validators=[MinValueValidator(0.00)]
    )
    objects = SupplierManager()


class SupplierCar(MainInformationMixin, CarInformationMixin):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    price = models.DecimalField(
        max_digits=12, decimal_places=2, validators=[MinValueValidator(0.00)]
    )
    count = models.IntegerField(default=1, validators=[MinValueValidator(0)])
    objects = SupplierCarManager()


class SupplierOffer(MainInformationMixin):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    max_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0.00)]
    )
    paid = models.BooleanField(default=False)
    objects = SupplierOfferManager()
