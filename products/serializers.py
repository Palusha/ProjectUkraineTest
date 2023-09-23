from rest_framework import serializers

from .models import Product


class ImagesListingField(serializers.RelatedField):
    def to_representation(self, value):
        request = self.context.get("request")
        return request.build_absolute_uri(value.image.url)


class ProductSerializer(serializers.ModelSerializer):
    userbars_items_number = serializers.SerializerMethodField()
    images = ImagesListingField(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ("id", "name", "userbars_items_number", "images")

    def get_userbars_items_number(self, obj):
        request = self.context.get("request")
        user = request.user
        if user.is_authenticated:
            user_bars_obj = obj.user_bars.filter(user=user).first()
            if user_bars_obj is not None:
                return user_bars_obj.items_number
        return 0
