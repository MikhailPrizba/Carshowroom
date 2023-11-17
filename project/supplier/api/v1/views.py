from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from supplier.models import Supplier, SupplierCar
from .serializer import SupplierSerializer, SupplierCarSerializer


class SupplierViewSet(viewsets.ModelViewSet):
    serializer_class = SupplierSerializer

    def get_queryset(self):
        return Supplier.objects.filter(is_active=True)

    def perform_create(self, serializer):
        Supplier.objects.create_instance(**serializer.data)

    def perform_destroy(self, instance):
        instance.soft_delete()


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
