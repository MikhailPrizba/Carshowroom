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
        Supplier.objects.soft_delete(instance)


@extend_schema(tags=["supplier_car/v1"])
class SupplierCarViewSet(viewsets.ModelViewSet):
    serializer_class = SupplierCarSerializer

    def get_queryset(self):
        return SupplierCar.objects.filter(
            supplier__user=self.request.user.pk, is_active=True
        )

    def perform_create(self, serializer):
        serializer.validated_data["supplier"] = Supplier.objects.get(
            user=self.request.user
        )
        serializer.save()

    def perform_destroy(self, instance):
        SupplierCar.objects.soft_delete(instance)
