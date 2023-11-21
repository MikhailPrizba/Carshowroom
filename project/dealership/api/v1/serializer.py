from rest_framework import serializers
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
    dealership = serializers.HiddenField(default=None)

    class Meta:
        model = DealershipCar
        fields = "__all__"


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
