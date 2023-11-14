from rest_framework import serializers
from dealership.models import Dealership, DealershipCar, DealershipOffer


class DealershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dealership
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


class DealershipCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealershipCar
        fields = (
            "id",
            "dealership",
            "mark",
            "model",
            "car_type",
            "color",
            "description",
            "price",
            "count",
            "is_active",
            "created",
            "updated",
        )


class DealershipOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = DealershipOffer
        fields = (
            "id",
            "customer",
            "dealership",
            "max_price",
            "paid",
            "is_active",
            "created",
            "updated",
        )
