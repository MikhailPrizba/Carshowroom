from rest_framework import viewsets
from drf_spectacular.utils import extend_schema
from supplier.models import Supplier, SupplierCar
from .serializer import SupplierSerializer, SupplierCarSerializer


@extend_schema(tags=["supplier/v1"])
class SupplierViewSet(viewsets.ModelViewSet):
    serializer_class = SupplierSerializer

    def get_queryset(self):
        return Supplier.objects.filter(is_active=True)

    def perform_create(self, serializer):
        Supplier.objects.create_instance(**serializer.data)

    def perform_destroy(self, instance):
        instance.soft_delete()


@extend_schema(tags=["supplier_car/v1"])
class SupplierCarViewSet(viewsets.ModelViewSet):
    serializer_class = SupplierCarSerializer

    def get_queryset(self):
        return Supplier.objects.filter(
            supplier__user=self.request.user.pk, is_active=True
        )

    def perform_create(self, serializer):
        serializer.validated_data["dealership"] = SupplierCar.objects.get(
            user=self.request.user
        )
        serializer.save()

    def perform_destroy(self, instance):
        instance.soft_delete()
