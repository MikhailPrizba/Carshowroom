from rest_framework import viewsets
from drf_spectacular.utils import extend_schema

from common.models import CustomQuerySet
from customer.models import Customer, CustomerOffer
from .serializer import CustomerSerializer, CustomerOfferSerializer
from .permissions import UpdatePermission, IsCustomerOrSuperUser
from rest_framework.permissions import IsAuthenticated


@extend_schema(tags=["customer/v1"])
class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.get_is_active()
    permission_classes = [IsAuthenticated]
    permission_classes_by_action = {
        "update": [UpdatePermission],
        "partial_update": [UpdatePermission],
    }

    def perform_create(self, serializer):
        Customer.objects.create_instance(**serializer.data)

    def perform_destroy(self, instance):
        Customer.objects.soft_delete(instance)


@extend_schema(tags=["customer_offer/v1"])
class CustomerOfferViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerOfferSerializer
    permission_classes = [IsAuthenticated, IsCustomerOrSuperUser]

    def get_queryset(self):
        return CustomerOffer.objects.get_is_active().filter(
            customer__user=self.request.user.pk
        )

    def perform_create(self, serializer):
        serializer.validated_data["customer"] = Customer.objects.get(
            user=self.request.user
        )
        serializer.save()

    def perform_destroy(self, instance):
        CustomerOffer.objects.soft_delete(instance)
