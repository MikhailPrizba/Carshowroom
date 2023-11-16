from django.urls import include, path
from rest_framework import routers

from supplier.api.v1.views import SupplierViewSet, SupplierCarViewSet

router = routers.DefaultRouter()
router.register(r"cars", SupplierCarViewSet, basename="supplier_cars")
router.register(r"", SupplierViewSet, basename="supplier")

urlpatterns = [
    path("", include(router.urls)),
]
