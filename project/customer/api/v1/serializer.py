from rest_framework import serializers
from common.serializer import CarSerializer
from customer.models import Customer, CustomerOffer
from user.api.v1.serializer import UserSerializer


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = "__all__"


class CustomerOfferSerializer(serializers.ModelSerializer):
    customer = serializers.HiddenField(default=None)

    class Meta:
        model = CustomerOffer
        fields = "__all__"
