from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class StoreTest(BaseTest):
    def test_create_store_items_empty(self):
        store = StoreModel("Test Store")

        self.assertListEqual(store.items.all(), [],
                             "The store's items lemgth was not 0 even though no items were added.")

    def test_crud(self):
        with self.app_context():
            store = StoreModel("Test Store")
            self.assertIsNone(StoreModel.find_by_name("Test Store"),
                              "Store with that name is found in the db, even though the store has not been added to the db.")

            store.save_to_db()

            self.assertIsNotNone(StoreModel.find_by_name("Test Store"),
                                 "Store with that name is not found in the db, even though the command for storing the store was run.")

            store.delete_from_db()

            self.assertIsNone(StoreModel.find_by_name("Test Store"),
                              "Store with that name is found in the db, even though the command for deleting the store was run.")

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel("Test Store")
            item = ItemModel("Test Item", 19.99, 1)
            store.save_to_db()
            item.save_to_db()
            self.assertEqual(store.items.count(), 1)
            self.assertEqual(store.items.first().name, 'Test Item')

    def test_store_json(self):
        store = StoreModel("test_store")
        expected = {
            "name": "test_store",
            "items": [],
        }

        self.assertDictEqual(expected, store.json())

    def test_store_json_with_items(self):
        with self.app_context():
            store = StoreModel("Test Store")
            item = ItemModel("Test Item", 19.99, 1)
            store.save_to_db()
            item.save_to_db()
            expected = {
                "name": "Test Store",
                "items": [
                    {
                        "name": "Test Item",
                        "price": 19.99,
                    }
                ],
            }

            self.assertDictEqual(expected, store.json())
