from decimal import Decimal
import uuid

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