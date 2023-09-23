from django_filters import rest_framework as filters
from django_filters import OrderingFilter


from .models import Product


class ProductFilter(filters.FilterSet):
    ordering = OrderingFilter(
        fields=(
            ("user_bars__items_number", "User bars items number"),
            ("name", "Name"),
        )
    )

    class Meta:
        model = Product
        fields = ("ordering",)
