from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from customer.models import Customer
from .serializer import CustomerSerializer


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

        return Response(status=status.HTTP_204_NO_CONTENT)
