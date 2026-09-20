from decimal import Decimal
import uuid
from data.product import ProductData


class TestProducts:
    def test_get_products_returns_paginated_catalog(self, api_manager):
        response = api_manager.products_api.get_products()

        data = response.json()
        assert data["total"] > 0
        assert len(data["items"]) <= data["size"]

    def test_products_price_filter(self, api_manager):
        response = api_manager.products_api.get_products(
            params={"price_min": 5000, "size": 100}
        )
        products = response.json()["items"]
        assert products, "Ожидали что будет хотя бы один товар дороже 5000 тысяч"

        for product in products:
            # цена приходит строкой - деньги сравниваем через Decimal (Тема 8)
            assert Decimal(product["price"]) >= 5000

    # Позитивный тест на получения карточки конкретного товара
    def test_product_id_is_valid(self, api_manager):

        # Получение конкретного id товара

        products = api_manager.products_api.get_products().json()["items"]
        product_id = products[0]["id"]

        response =  api_manager.products_api.get_product(product_id)

        assert response.json()["id"] == product_id

    # Негативный тест с неправильным product_id
    def test_product_is_invalid(self, api_manager):
        response = api_manager.products_api.get_product(uuid.uuid4(), expected_status=404)

        assert response.json()["error"]["code"] == "PRODUCT_NOT_FOUND"

    def test_created_product_is_available(self, api_manager, created_product):
        product_id = created_product["id"]

        response = api_manager.products_api.get_product(product_id)

        assert response.json()["id"] == product_id, "id товара не совпало"


    #Позитивный тест на создание товара
    def test_product_creation_by_the_admin(self, api_manager, authenticated_admin, category_id):
        product_data = ProductData.creation_product_data(category_id)

        create_response = api_manager.products_api.create_product(product_data)

        product_id = create_response.json()["id"]

        delete_response = api_manager.products_api.delete_product(product_id)

    # Негативный тест на создание товара
    def test_product_creation_by_the_user(self, api_manager, authenticated_user, category_id):
        product_data = ProductData.creation_product_data(category_id)

        response = api_manager.products_api.create_product(product_data, expected_status=403)

        assert response.json()["error"]["code"] == "FORBIDDEN"

    # Позитивный тест на изменение товара
    def test_product_update_by_admin(self, api_manager, created_product, authenticated_admin):
        product_id = created_product["id"]
        patch_data = {
            "name": "mya mya mya gav gav",
        }

        response = api_manager.products_api.update_product(product_id, patch_data)

    # Негативный тест на изменение товара
    def test_product_price_change(self, api_manager, created_product, authenticated_admin):
        product_id = created_product["id"]
        patch_data = {
            "price": 50000,
        }

        response = api_manager.products_api.update_product(product_id, patch_data, expected_status=422)

        assert response.json()["detail"][0]["type"] == "extra_forbidden"

    # Позитивный тест на изменение товара
    def test_update_price_by_admin(self, api_manager,created_product, authenticated_admin):
        product_id = created_product["id"]
        old_price = created_product["price"]
        price_data = {
            "price": 5200,
        }

        response = api_manager.products_api.update_price(product_id, price_data)

        assert response.json()["price"] != old_price

    # Негативный тест на изменение товара
    def test_update_price_by_manager(self, api_manager, authenticated_manager, created_product):
        product_id = created_product["id"]

        patch_response = api_manager.products_api.update_price(product_id, {"price": 2000}, expected_status=403)

        assert patch_response.json()["error"]["code"] == "FORBIDDEN"

    def test_delete_product_by_admin(self, api_manager, authenticated_admin, category_id):
        product_data = ProductData.creation_product_data(category_id)

        create_response = api_manager.products_api.create_product(product_data)

        product_id = create_response.json()["id"]

        delete_response = api_manager.products_api.delete_product(product_id)

    def test_negative_delete_product_by_manager(self, api_manager, created_product, authenticated_manager):
        product_id = created_product["id"]

        delete_response = api_manager.products_api.delete_product(product_id, expected_status=403)

        assert delete_response.json()["error"]["code"] == "FORBIDDEN"

    def test_negative_delete_seed_product(self, api_manager, authenticated_admin, seed_product_id):
        delete_response = api_manager.products_api.delete_product(seed_product_id, expected_status=403)

        assert delete_response.json()["error"]["code"] == "SEED_PROTECTED"