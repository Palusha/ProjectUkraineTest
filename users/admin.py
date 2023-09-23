from django.contrib import admin

from .models import UserBar


@admin.register(UserBar)
class UserBarAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product", "items_number")
    list_display_links = ("id", "user", "product", "items_number")
