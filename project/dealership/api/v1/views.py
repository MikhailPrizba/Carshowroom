from rest_framework import viewsets
from drf_spectacular.utils import extend_schema

from dealership.models import Dealership, DealershipCar, DealershipOffer
from .serializer import (
    DealershipSerializer,
    DealershipCarSerializer,
    DealershipOfferSerializer,
)


@extend_schema(tags=["dealership/v1"])
class DealershipViewSet(viewsets.ModelViewSet):
    serializer_class = DealershipSerializer

    def get_queryset(self):
        return Dealership.objects.filter(is_active=True)

    def perform_create(self, serializer):
        Dealership.objects.create_instance(**serializer.data)

    def perform_destroy(self, instance):
        Dealership.objects.soft_delete(instance)


@extend_schema(tags=["dealership_car/v1"])
class DealershipCarViewSet(viewsets.ModelViewSet):
    serializer_class = DealershipCarSerializer

    def get_queryset(self):
        return DealershipCar.objects.filter(
            dealership__user=self.request.user.pk, is_active=True
        )

    def perform_create(self, serializer):
        serializer.validated_data["dealership"] = Dealership.objects.get(
            user=self.request.user
        )
        serializer.save()

    def perform_destroy(self, instance):
        DealershipCar.objects.soft_delete(instance)


@extend_schema(tags=["dealership_offer/v1"])
class DealershipOfferViewSet(viewsets.ModelViewSet):
    serializer_class = DealershipOfferSerializer

    def get_queryset(self):
        return DealershipOfferSerializer.objects.filter(
            dealership__user=self.request.user.pk, is_active=True
        )

    def perform_destroy(self, instance):
        DealershipOffer.objects.soft_delete(instance)
