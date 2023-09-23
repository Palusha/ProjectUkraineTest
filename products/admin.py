from django.contrib import admin

from .models import Product, ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "in_trash")
    list_display_links = ("id", "name", "in_trash")
    list_filter = ("in_trash",)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "image")
    list_display_links = ("id", "product", "image")
