from rest_framework import serializers
from customer.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
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
