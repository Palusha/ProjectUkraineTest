from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255, null=False)
    in_trash = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="uploads/%d-%m-%Y/")

    def __str__(self):
        return self.image.name

    class Meta:
        verbose_name = "product image"
        verbose_name_plural = "products images"
