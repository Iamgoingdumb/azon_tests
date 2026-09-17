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
def created_product(api_manager, authenticated_admin, category_id):
    product_data = ProductData.creation_product_data(category_id)
    response = api_manager.products_api.create_product(product_data)
    product = {**product_data, "id": response.json()["id"]}
    yield product
    api_manager.products_api.delete_product(product["id"])
