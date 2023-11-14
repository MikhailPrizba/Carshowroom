from django.urls import include, path
from rest_framework import routers

from customer.api.v1.views import CustomerViewSet

router = routers.DefaultRouter()
router.register(r"", CustomerViewSet, basename="customer")

urlpatterns = [
    path("", include(router.urls)),
]
