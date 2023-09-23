import pytest
from django.urls import reverse

from users.models import UserBar


@pytest.mark.django_db
class TestUserBarRetriveUpdate:
    @pytest.fixture
    def url(self, product):
        return reverse(
            "users:userbar-retrieve-update", kwargs={"product_id": product.id}
        )

    def test_user_bar_returns_data(self, client, create_user_bar, product, user, url):
        user_bar = create_user_bar(product=product, user=user)

        client.login(username=user.username, password="password")
        response = client.get(url)

        response_data = response.json()

        assert response.status_code == 200
        assert response_data["id"] == user_bar.id
        assert response_data["items_number"] == user_bar.items_number
        assert response_data["user"] == user.id
        assert response_data["product"] == product.id

    def test_user_bar_is_created_if_one_with_passed_product_does_not_exists(
        self, client, create_product, user
    ):
        product = create_product()

        assert not UserBar.objects.filter(user=user, product=product).exists()

        client.login(username=user.username, password="password")
        response = client.get(f"/users/user_bar/{product.id}/")

        assert UserBar.objects.filter(user=user, product=product).exists()

        response_data = response.json()

        assert "id" in response_data
        assert response_data["items_number"] == 1
        assert response_data["user"] == user.id
        assert response_data["product"] == product.id

    def test_raises_a_validation_error_if_user_tries_to_set_items_number_to_zero(
        self, client, user, url
    ):
        client.login(username=user.username, password="password")
        response = client.put(
            url, data={"items_number": 0}, content_type="application/json"
        )
        assert response.status_code == 400

        response_data = response.json()

        assert "Ensure this value is greater than 0." in response_data["items_number"]

    def test_returns_not_found_if_user_is_not_authenticated(self, client, url):
        response = client.get(url)

        assert response.status_code == 404

        response_data = response.json()

        assert response_data == {"detail": "Not found."}
