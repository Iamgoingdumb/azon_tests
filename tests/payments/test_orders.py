import pytest


class TestOrders:

    def test_new_user_has_no_orders(self, api_manager, authenticated_user):
        response = api_manager.payment_api.get_orders()

        data = response.json()
        assert data["total"] == 0
        assert data["items"] == []


    @pytest.mark.parametrize(
        "client_name",
        ["auth_api", "products_api", "payment_api"],
    )
    def test_health(self,api_manager, client_name ):
        client = getattr(api_manager, client_name)

