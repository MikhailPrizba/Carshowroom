from django.contrib import admin
from .models import Dealership, DealershipCar

# Register your models here.
admin.site.register(DealershipCar)
admin.site.register(Dealership)
