from django_filters import rest_framework as filters
from rest_framework import generics

from .filters import ProductFilter
from .models import Product
from .serializers import ProductSerializer


class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(in_trash=False).prefetch_related("images")
