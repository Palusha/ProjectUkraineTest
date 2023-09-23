from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path(
        "user_bar/<int:product_id>/",
        views.UserBarRetriveUpdate.as_view(),
        name="userbar-retrieve-update",
    ),
]
