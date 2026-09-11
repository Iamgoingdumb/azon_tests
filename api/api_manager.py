#api/api_manager.py
from api.auth_api import AuthAPI
from api.payment_api import PaymentAPI
from api.products_api import ProductAPI
from api.user_api import UserAPI

class ApiManager:
    """Единая точка доступа ко всем API стенда"""

    def __init__(self, session):
        self.session = session
        self.auth_api = AuthAPI(session)
        self.products_api = ProductAPI(session)
        self.payment_api = PaymentAPI(session)
        self.user_api = UserAPI(session)
