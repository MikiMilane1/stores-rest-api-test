from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class ItemTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            store = StoreModel("Test Store")
            store.save_to_db()
            item = ItemModel("Test Name", 19.00, 1)
            self.assertIsNone(ItemModel.find_by_name("Test Name"),
                              "Found an item with the name 'Test Name', but expected not to.")
            item.save_to_db()
            self.assertIsNotNone(ItemModel.find_by_name("Test Name"),
                                 "Did not find an item with the name 'Test Name', but expected to.")
            item.delete_from_db()
            self.assertIsNone(ItemModel.find_by_name("Test Name"),
                              "Found an item with the name 'Test Name', but expected not to.")

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel("Test Store")
            item = ItemModel('Test Item', 19.99, 1)
            store.save_to_db()
            item.save_to_db()

            self.assertEqual(item.store.name, "Test Store")
