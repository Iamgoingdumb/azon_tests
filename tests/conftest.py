import requests
import pytest

from api.api_manager import ApiManager, CategoriesAPI
from data.product import ProductData
from data.users import UserData


@pytest.fixture
def api_manager():
    session = requests.Session()
    yield ApiManager(session)
    session.close()

@pytest.fixture(autouse=True)
def clear_authorization_after_test(api_manager):
    yield
    api_manager.session.headers.pop("Authorization", None)

@pytest.fixture
def registered_user(api_manager):
    user_data = UserData.registration_data()
    response = api_manager.auth_api.register_user(user_data)
    return {**user_data, "id": response.json()["id"]}

@pytest.fixture
def registered_manager(api_manager):
    user_data = UserData.registration_manager_data()
    response = api_manager.auth_api.register_user(user_data)
    return {**user_data, "id": response.json()["id"]}

@pytest.fixture
def registered_admin(api_manager):
    user_data = UserData.registration_admin_data()
    response = api_manager.auth_api.register_user(user_data)
    return {**user_data, "id": response.json()["id"]}

@pytest.fixture
def authenticated_user(api_manager):
    user_data = UserData.registration_data()

    register_response = api_manager.auth_api.register_user(user_data)

    api_manager.auth_api.authenticate((user_data["email"], user_data["password"]))

    return {**user_data, "id": register_response.json()["id"]}

@pytest.fixture
def authenticated_manager(api_manager):
    user_data = UserData.registration_manager_data()

    register_response = api_manager.auth_api.register_user(user_data)

    api_manager.auth_api.authenticate((user_data["email"], user_data["password"]))

    return {**user_data, "id": register_response.json()["id"]}

@pytest.fixture
def authenticated_admin(api_manager):
    user_data = UserData.registration_admin_data()

    register_response = api_manager.auth_api.register_user(user_data)

    api_manager.auth_api.authenticate((user_data["email"], user_data["password"]))

    return {**user_data, "id": register_response.json()["id"]}

@pytest.fixture
def category_id(api_manager):
    response = api_manager.categories_api.get_categories()

    categories = response.json()
    assert categories, "Список пуст"
    return categories[-1]["id"]

@pytest.fixture
def created_product(admin_manager , category_id):
    product_data = ProductData.creation_product_data(category_id)
    response = admin_manager.products_api.create_product(product_data)
    product = {**product_data, "id": response.json()["id"]}
    yield product
    admin_manager.products_api.delete_product(product["id"])

@pytest.fixture
def admin_manager():
    admin_session = requests.Session()
    manager = ApiManager(admin_session)

    admin_credentials = UserData.registration_admin_data()

    manager.auth_api.register_user(admin_credentials)

    manager.auth_api.authenticate((admin_credentials["email"], admin_credentials["password"]))

    yield manager

    admin_session.close()

@pytest.fixture
def seed_product_id(api_manager):
    params = {
        "search": "Умные часы AZON Watch 5",
        "price_min": 5499,
        "in_stock": True,
        "page": 1,
        "size": 20,
    }

    response = api_manager.products_api.get_products(params)

    product_id = response.json()["items"][0]["id"]
    return product_id
