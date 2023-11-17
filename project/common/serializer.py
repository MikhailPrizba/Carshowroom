from rest_framework import serializers


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        car_fields = [
            "id",
            "mark",
            "model",
            "car_type",
            "color",
            "description",
            "is_active",
            "created",
            "updated",
        ]
