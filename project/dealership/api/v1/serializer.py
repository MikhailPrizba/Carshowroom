from rest_framework import serializers
from common.serializer import CarSerializer
from dealership.models import Dealership, DealershipCar, DealershipOffer
from user.api.v1.serializer import UserSerializer


class DealershipSerializer(serializers.ModelSerializer):
    user = UserSerializer()

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
        # "dealership",
        fields = CarSerializer.Meta.car_fields + ["price", "count"]


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
