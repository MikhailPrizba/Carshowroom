from rest_framework import serializers
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
    class Meta:
        model = CustomerOffer
        fields = (
            "id",
            "mark",
            "model",
            "car_type",
            "color",
            "description",
            "max_price",
            "is_active",
            "created",
            "updated",
        )
