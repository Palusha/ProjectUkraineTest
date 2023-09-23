from rest_framework import serializers

from .models import UserBar


class UserBarSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBar
        fields = ("id", "items_number", "user", "product")
        read_only_fields = (
            "product",
            "user",
        )

    def validate_items_number(self, value):
        if value == 0:
            raise serializers.ValidationError("You cannot set value to zero.")
        return value
