#utils/data_generator.py
import uuid
from faker import Faker

fake = Faker("en_US")


class DataGenerator:

    @staticmethod
    def generate_email():
        #uuid4 гарантирует уникальность даже на общем стенде - прием из Темы 8
        return f"dumb-{uuid.uuid4().hex[:8]}@icloud.com"

    @staticmethod
    def generate_password():
        return fake.password(length=12)

    @staticmethod
    def generate_full_name():
        return fake.name()

    @staticmethod
    def generate_product_name():
        return f"Лампа AZON {uuid.uuid4().hex[:4]}"

    @staticmethod
    def generate_sku():
        return f"{uuid.uuid4().hex[:10]}"

    @staticmethod
    def generate_description():
        return fake.sentence(nb_words=8)

    @staticmethod
    def generate_price():
        return fake.random_int(min=1000, max=50000)

    @staticmethod
    def generate_stock():
        return fake.random_int(min=2, max=90)