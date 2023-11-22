from rest_framework import serializers
from common.serializer import CarSerializer
from customer.models import Customer, CustomerOffer
from user.api.v1.serializer import UserSerializer


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = (
            "id",
            "user",
            "balance",
            "email_confirm",
            "phone_number",
            "location",
            "is_active",
            "created",
            "updated",
        )


class CustomerOfferSerializer(serializers.ModelSerializer):
    customer = serializers.HiddenField(default=None)

    class Meta:
        model = CustomerOffer
        fields = CarSerializer.Meta.fields + [
            "customer",
            "max_price",
        ]
