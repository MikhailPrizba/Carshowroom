from rest_framework import viewsets

from customer.models import Customer, CustomerOffer
from .serializer import CustomerSerializer, CustomerOfferSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer

    def get_queryset(self):
        return Customer.objects.filter(is_active=True)

    def perform_create(self, serializer):
        Customer.objects.create_instance(**serializer.data)

    def perform_destroy(self, instance):
        instance.soft_delete()


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

    def perform_destroy(self, instance):
        instance.soft_delete()
