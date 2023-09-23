from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import models


def validate_greater_zero(value):
    if value <= 0:
        raise ValidationError(
            _("Ensure this value is greater than 0."),
        )


class UserBar(models.Model):
    user = models.ForeignKey(
        get_user_model(), related_name="user_bars", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        "products.Product", related_name="user_bars", on_delete=models.CASCADE
    )
    items_number = models.IntegerField(default=1, validators=[validate_greater_zero])

    class Meta:
        unique_together = ("user", "product")

    def __str__(self):
        return f"{self.user.username}-{self.product.name}"
