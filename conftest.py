import pytest

from django.contrib.auth import get_user_model
from faker import Faker

from products.models import Product, ProductImage
from users.models import UserBar


@pytest.fixture
def faker():
    return Faker()


@pytest.fixture
def create_user(faker):
    def _create_user(*args, **kwargs):
        if not kwargs:
            user_data = {
                "username": faker.first_name().lower(),
                "email": faker.email(),
                "password": faker.password(),
            }
        user_data.update(kwargs)
        return get_user_model().objects.create(**user_data)

    return _create_user


@pytest.fixture
def user():
    User = get_user_model()
    user = User(username="user", email="user@example.com")
    user.set_password("password")
    user.save()
    return user


@pytest.fixture
def create_product(faker):
    def _create_product(*args, **kwargs):
        product_data = {"name": faker.text(max_nb_chars=10), "in_trash": False}
        product_data.update(kwargs)
        return Product.objects.create(**product_data)

    return _create_product


@pytest.fixture
def product(create_product):
    return create_product()


@pytest.fixture
def create_user_bar(faker, create_product, create_user):
    def _create_user_bar(*args, **kwargs):
        product_data = {
            "product": kwargs.get("product") or create_product(),
            "user": kwargs.get("user") or create_user(),
            "items_number": kwargs.get("items_number") or faker.pyint(),
        }
        return UserBar.objects.create(**product_data)

    return _create_user_bar


@pytest.fixture
def create_product_image(faker, create_product):
    def _create_product_image(*args, **kwargs):
        product_data = {
            "product": kwargs.get("product") or create_product(),
            "image": faker.image_url(),
        }
        return ProductImage.objects.create(**product_data)

    return _create_product_image
