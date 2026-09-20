class TestCategories:

    def test_category_id_belongs_to_categories(self, api_manager, category_id):
        response = api_manager.categories_api.get_categories()
        categories = response.json()

        all_categories_id = [category["id"] for category in categories]
        assert category_id in all_categories_id
