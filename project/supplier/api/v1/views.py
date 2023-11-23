from rest_framework import viewsets
from drf_spectacular.utils import extend_schema
from supplier.models import Supplier, SupplierCar
from .serializer import SupplierSerializer, SupplierCarSerializer
from .permissions import UpdatePermission, IsDealershipOrSuperUser
from rest_framework.permissions import IsAuthenticated


@extend_schema(tags=["supplier/v1"])
class SupplierViewSet(viewsets.ModelViewSet):
    serializer_class = SupplierSerializer
    queryset = Supplier.objects.get_is_active()
    permission_classes = [IsAuthenticated]
    permission_classes_by_action = {
        "update": [UpdatePermission],
        "partial_update": [UpdatePermission],
    }

    def perform_create(self, serializer):
        Supplier.objects.create_instance(**serializer.data)

    def perform_destroy(self, instance):
        Supplier.objects.soft_delete(instance)


@extend_schema(tags=["supplier_car/v1"])
class SupplierCarViewSet(viewsets.ModelViewSet):
    serializer_class = SupplierCarSerializer
    permission_classes = [IsAuthenticated, IsDealershipOrSuperUser]

    def get_queryset(self):
        return SupplierCar.objects.get_is_active().filter(
            supplier__user=self.request.user.pk
        )

    def perform_create(self, serializer):
        serializer.validated_data["supplier"] = Supplier.objects.get(
            user=self.request.user
        )
        serializer.save()

    def perform_destroy(self, instance):
        SupplierCar.objects.soft_delete(instance)
