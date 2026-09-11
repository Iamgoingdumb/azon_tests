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

