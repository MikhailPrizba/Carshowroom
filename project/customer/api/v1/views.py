from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from customer.models import Customer, CustomerOffer
from .serializer import CustomerSerializer, CustomerOfferSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer

    def get_queryset(self):
        return Customer.objects.filter(is_active=True)

    def perform_create(self, serializer):
        Customer.objects.create_instance(**serializer.data)

    def delete(self, request, pk=None):
        instance = self.get_object()

        instance.is_active = False
        instance.save()


class CustomerOfferViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerOfferSerializer

    def get_queryset(self):
        return CustomerOffer.objects.filter(
            customer__user=self.request.user.pk, is_active=True
        )

    def perform_create(self, serializer):
        serializer.validated_data["customer"] = Customer.objects.get(
            user=self.request.user
        )
        serializer.save()

    def destroy(self, request, pk=None):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
