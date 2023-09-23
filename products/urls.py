from django.urls import path

from . import views

app_name = "products"

urlpatterns = [
    path("", views.ProductList.as_view(), name="products-list"),
]
