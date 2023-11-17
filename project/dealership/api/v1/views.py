from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from dealership.models import Dealership, DealershipCar
from .serializer import (
    DealershipSerializer,
    DealershipCarSerializer,
    DealershipOfferSerializer,
)
from django.db.models import Q


class DealershipViewSet(viewsets.ModelViewSet):
    serializer_class = DealershipSerializer

    def get_queryset(self):
        return Dealership.objects.filter(is_active=True)

    def perform_create(self, serializer):
        Dealership.objects.create_instance(**serializer.data)

    def destroy(self, request, pk=None):
        instance = self.get_object()

        instance.is_active = False
        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


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
        instance.soft_delete()


class DealershipOfferViewSet(viewsets.ModelViewSet):
    serializer_class = DealershipOfferSerializer

    def get_queryset(self):
        return DealershipOfferSerializer.objects.filter(
            dealership__user=self.request.user.pk, is_active=True
        )

    def perform_destroy(self, instance):
        instance.soft_delete()
