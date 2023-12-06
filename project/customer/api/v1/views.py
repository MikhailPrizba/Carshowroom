from rest_framework import viewsets
from drf_spectacular.utils import extend_schema
from customer.models import Customer, CustomerOffer
from .serializer import CustomerSerializer, CustomerOfferSerializer
from .permissions import UpdatePermission, IsCustomerOrSuperUser
from rest_framework.permissions import IsAuthenticated


@extend_schema(tags=["customer/v1"])
class CustomerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows customers to be viewed or edited.

    This viewset provides CRUD operations for the Customer model.
    """

    serializer_class = CustomerSerializer
    queryset = Customer.objects.get_is_active()
    permission_classes = [IsAuthenticated]
    permission_classes_by_action = {
        "update": [UpdatePermission],
        "partial_update": [UpdatePermission],
    }

    def perform_create(self, serializer):
        """
        Perform create operation for the Customer model.

        Args:
            serializer: The serializer instance.

        Note:
            This method is called during the creation of a new Customer instance.
        """
        Customer.objects.create_instance(**serializer.data)

    def perform_destroy(self, instance):
        """
        Perform destroy operation for the Customer model.

        Args:
            instance: The Customer instance to be destroyed.

        Note:
            This method is called during the deletion of a Customer instance.
        """
        Customer.objects.soft_delete(instance)


@extend_schema(tags=["customer_offer/v1"])
class CustomerOfferViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows customer offers to be viewed or edited.

    This viewset provides CRUD operations for the CustomerOffer model.
    """

    serializer_class = CustomerOfferSerializer
    permission_classes = [IsAuthenticated, IsCustomerOrSuperUser]

    def get_queryset(self):
        """
        Get the queryset for CustomerOffer.

        Returns:
            Queryset: Filtered queryset based on the request user.
        """
        return CustomerOffer.objects.get_is_active().filter(
            customer__user=self.request.user.pk
        )

    def perform_create(self, serializer):
        """
        Perform create operation for the CustomerOffer model.

        Args:
            serializer: The serializer instance.

        Note:
            This method is called during the creation of a new CustomerOffer instance.
        """
        serializer.validated_data["customer"] = Customer.objects.get(
            user=self.request.user
        )
        CustomerOffer.objects.create_instance(**serializer.validated_data)

    def perform_destroy(self, instance):
        """
        Perform destroy operation for the CustomerOffer model.

        Args:
            instance: The CustomerOffer instance to be destroyed.

        Note:
            This method is called during the deletion of a CustomerOffer instance.
        """
        CustomerOffer.objects.soft_delete(instance)
