from django.db import models
from django_enum import TextChoices
from django.contrib.auth.models import AbstractUser
# Create your models here.



class User(AbstractUser):
    class UserRoleChoices(TextChoices):
        UNKNOWN = 'UNKNOWN'
        ADMIN = 'ADMIN'
        SUPPLIER = 'SUPPLIER'
        DEALERSHIP = 'DEALERSHIP'
        CUSTOMER = 'CUSTOMER'
        
    
    user_role = models.TextField(
        choices=UserRoleChoices.choices, default=UserRoleChoices.UNKNOWN)
    
    def __str__(self):
        return self.username