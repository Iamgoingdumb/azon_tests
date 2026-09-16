
from utils.data_generator import DataGenerator


class ProductData:
    """Object Mother для тел запросов product API"""

    @staticmethod
    def creation_product_data(category_id):
        return {
            "name": DataGenerator.generate_gadget_name(),
            "sku": DataGenerator.generate_sku(),
            "description": DataGenerator.generate_description(),
            "price": DataGenerator.generate_price(),
            "stock": DataGenerator.generate_stock(),
            "category_id": category_id,
        }