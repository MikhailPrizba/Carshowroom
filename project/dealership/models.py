from common.models import (
    CarInformationMixin,
    MainInformationMixin,
    UserInformationMixin,
)
from customer.models import Customer
from django.core.validators import MinValueValidator
from django.db import models
from user.models import User

class DealershipManager(models.Manager):
    def create_instance(self,  username, email, password,**kwargs):
        user = User.objects.create_user(username=username, email=email, password=password)
        kwargs['user'] = user
        return self.create(**kwargs)

    def update_instance(self, id,**kwargs):
        self.filter(id=id).update(**kwargs)
        return self.get(id=id)
        

class DealershipCarManager(models.Manager):
    def create_instance(self,  **kwargs):
        return self.create(**kwargs)

    def update_instance(self, id,**kwargs):
        self.filter(id=id).update(**kwargs)
        return self.get(id=id)
    
class DealershipOfferManager(models.Manager):
    def create_instance(self,  **kwargs):
        return self.create(**kwargs)

    def update_instance(self, id,**kwargs):
        self.filter(id=id).update(**kwargs)
        return self.get(id=id)
    
class Dealership(MainInformationMixin, UserInformationMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(
        default=0, max_digits=12, decimal_places=2, validators=[MinValueValidator(0.00)]
    )
    objects = DealershipManager()


class ShopCar(MainInformationMixin, CarInformationMixin):
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    price = models.DecimalField(
        default=0, max_digits=12, decimal_places=2, validators=[MinValueValidator(0.00)]
    )
    count = models.IntegerField(default=1, validators=[MinValueValidator(0)])
    objects = DealershipCarManager()

class ShopOffer(MainInformationMixin):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE)
    max_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0.00)]
    )
    paid = models.BooleanField(default=False)
    objects = DealershipOfferManager()