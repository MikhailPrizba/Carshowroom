from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from common.models import MainInformationMixin, UserInformationMixin
from user.models import User


class CustomerManager(models.Manager):
    def create_instance(self,  username, email, password,**kwargs):
        user = User.objects.create_user(username=username, email=email, password=password)
        kwargs['user'] = user
        return self.create(**kwargs)

    def update_instance(self, id,**kwargs):
        self.filter(id=id).update(**kwargs)
        return self.get(id=id)

    

class Customer(MainInformationMixin, UserInformationMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2, validators=[MinValueValidator(0.00)])
    objects = CustomerManager()
