import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestListProducts:
    @pytest.fixture
    def url(self):
        return reverse("products:products-list")

    def test_product_in_trash_is_now_shown(self, client, create_product, url):
        product = create_product()
        product_in_trash = create_product(in_trash=True)

        response = client.get(url)
        response_data = response.json()
        results = response_data.get("results", [])

        assert response.status_code == 200
        assert len(results) == 1

        r_product = results[0]

        assert r_product["id"] == product.id
        assert r_product["name"] == product.name
        assert r_product["userbars_items_number"] == 0

    def test_userbars_items_number_equals_zero_if_current_user_does_not_have_a_user_bar_with_product(
        self, client, create_product, create_user, create_user_bar, user, url
    ):
        f_prod = create_product()
        s_prod = create_product()
        new_user = create_user()

        cur_user_bar = create_user_bar(product=f_prod, user=user)
        new_user_bar = create_user_bar(product=s_prod, user=new_user)

        client.login(username=user.username, password="password")

        response = client.get(url)
        response_data = response.json()
        results = response_data.get("results", [])

        assert response.status_code == 200
        assert len(results) == 2

        rf_prod, rs_prod = results

        assert rf_prod["id"] == f_prod.id
        assert rf_prod["name"] == f_prod.name
        assert (
            rf_prod["userbars_items_number"]
            == f_prod.user_bars.filter(user=user).first().items_number
        )
        assert rf_prod["images"] == []

        assert rs_prod["id"] == s_prod.id
        assert rs_prod["name"] == s_prod.name
        assert rs_prod["userbars_items_number"] == 0
        assert rs_prod["images"] == []

    def test_product_contains_list_of_urls(
        self, client, create_product, create_product_image, url
    ):
        f_prod = create_product()

        fpi = create_product_image(product=f_prod)
        spi = create_product_image(product=f_prod)
        tpi = create_product_image(product=f_prod)

        expected_images_urls = []
        for pi in [fpi, spi, tpi]:
            expected_images_urls.append("http://testserver" + pi.image.url)

        response = client.get(url)
        response_data = response.json()
        results = response_data.get("results", [])

        assert response.status_code == 200
        assert len(results) == 1

        r_prod = results[0]

        assert r_prod["id"] == f_prod.id
        assert r_prod["name"] == f_prod.name
        assert r_prod["userbars_items_number"] == 0
        assert r_prod["images"] == expected_images_urls

    def test_orders_by_name(self, client, create_product, url):
        f_prod = create_product(name="BBB")
        s_prod = create_product(name="AAA")
        t_prod = create_product(name="CCC")

        response = client.get(url + "?ordering=Name")
        response_data = response.json()
        results = response_data.get("results", [])

        assert response.status_code == 200
        assert len(results) == 3

        fr_prod, sr_prod, tr_prod = results

        assert fr_prod["id"] == s_prod.id
        assert fr_prod["name"] == s_prod.name
        assert fr_prod["userbars_items_number"] == 0
        assert fr_prod["images"] == []

        assert sr_prod["id"] == f_prod.id
        assert sr_prod["name"] == f_prod.name
        assert sr_prod["userbars_items_number"] == 0
        assert sr_prod["images"] == []

        assert tr_prod["id"] == t_prod.id
        assert tr_prod["name"] == t_prod.name
        assert tr_prod["userbars_items_number"] == 0
        assert tr_prod["images"] == []

    def test_orders_by_name_descending(self, client, create_product, url):
        f_prod = create_product(name="BBB")
        s_prod = create_product(name="AAA")
        t_prod = create_product(name="CCC")

        response = client.get(url + "?ordering=-Name")
        response_data = response.json()
        results = response_data.get("results", [])

        assert response.status_code == 200
        assert len(results) == 3

        fr_prod, sr_prod, tr_prod = results

        assert fr_prod["id"] == t_prod.id
        assert fr_prod["name"] == t_prod.name
        assert fr_prod["userbars_items_number"] == 0
        assert fr_prod["images"] == []

        assert sr_prod["id"] == f_prod.id
        assert sr_prod["name"] == f_prod.name
        assert sr_prod["userbars_items_number"] == 0
        assert sr_prod["images"] == []

        assert tr_prod["id"] == s_prod.id
        assert tr_prod["name"] == s_prod.name
        assert tr_prod["userbars_items_number"] == 0
        assert tr_prod["images"] == []

    def test_orders_by_userbars_items_number(
        self, client, create_product, create_user_bar, user, url
    ):
        f_prod = create_product(name="BBB")
        s_prod = create_product(name="AAA")
        t_prod = create_product(name="CCC")

        f_user_bar = create_user_bar(user=user, product=f_prod, items_number=20)
        s_user_bar = create_user_bar(user=user, product=s_prod, items_number=30)
        t_user_bar = create_user_bar(user=user, product=t_prod, items_number=10)

        client.login(username=user.username, password="password")
        response = client.get(url + "?ordering=User+bars+items+number")
        response_data = response.json()
        results = response_data.get("results", [])

        assert response.status_code == 200
        assert len(results) == 3

        fr_prod, sr_prod, tr_prod = results

        assert fr_prod["id"] == t_prod.id
        assert fr_prod["name"] == t_prod.name
        assert fr_prod["userbars_items_number"] == t_user_bar.items_number
        assert fr_prod["images"] == []

        assert sr_prod["id"] == f_prod.id
        assert sr_prod["name"] == f_prod.name
        assert sr_prod["userbars_items_number"] == f_user_bar.items_number
        assert sr_prod["images"] == []

        assert tr_prod["id"] == s_prod.id
        assert tr_prod["name"] == s_prod.name
        assert tr_prod["userbars_items_number"] == s_user_bar.items_number
        assert tr_prod["images"] == []

    def test_orders_by_userbars_items_number_descending(
        self, client, create_product, create_user_bar, user, url
    ):
        f_prod = create_product(name="BBB")
        s_prod = create_product(name="AAA")
        t_prod = create_product(name="CCC")

        f_user_bar = create_user_bar(user=user, product=f_prod, items_number=20)
        s_user_bar = create_user_bar(user=user, product=s_prod, items_number=30)
        t_user_bar = create_user_bar(user=user, product=t_prod, items_number=10)

        client.login(username=user.username, password="password")
        response = client.get(url + "?ordering=-User+bars+items+number")
        response_data = response.json()
        results = response_data.get("results", [])

        assert response.status_code == 200
        assert len(results) == 3

        fr_prod, sr_prod, tr_prod = results

        assert fr_prod["id"] == s_prod.id
        assert fr_prod["name"] == s_prod.name
        assert fr_prod["userbars_items_number"] == s_user_bar.items_number
        assert fr_prod["images"] == []

        assert sr_prod["id"] == f_prod.id
        assert sr_prod["name"] == f_prod.name
        assert sr_prod["userbars_items_number"] == f_user_bar.items_number
        assert sr_prod["images"] == []

        assert tr_prod["id"] == t_prod.id
        assert tr_prod["name"] == t_prod.name
        assert tr_prod["userbars_items_number"] == t_user_bar.items_number
        assert tr_prod["images"] == []
