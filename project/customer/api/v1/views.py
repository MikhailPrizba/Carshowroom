from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from customer.models import Customer
from .serializer import CustomerSerializer


class CustomerViewSet(
    viewsets.GenericViewSet,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
):
    serializer_class = CustomerSerializer

    def get_queryset(self):
        return Customer.objects.filter(is_active=True)

    def perform_create(self, serializer):
        Customer.objects.create_instance(**serializer.data)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk=None):
        instance = self.get_object()

        instance.is_active = False
        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
