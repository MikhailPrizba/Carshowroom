from rest_framework import serializers
from supplier.models import Supplier, SupplierCar, SupplierOffer
from user.api.v1.serializer import UserSerializer


class SupplierSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Supplier
        fields = (
            "id",
            "user",
            "foundation_year",
            "balance",
            "email_confirm",
            "phone_number",
            "location",
            "is_active",
            "created",
            "updated",
        )


class SupplierCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierCar
        fields = (
            "id",
            "supplier",
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


class SupplierOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierOffer
        fields = (
            "id",
            "dealership",
            "supplier",
            "max_price",
            "paid",
            "is_active",
            "created",
            "updated",
        )
