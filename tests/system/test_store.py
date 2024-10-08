from models.store import StoreModel
from models.item import ItemModel

from tests.base_test import BaseTest
import json


class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post("/store/test_store")

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name("test_store"))
                self.assertDictEqual({"name": "test_store", "items": []}, StoreModel.find_by_name("test_store").json())

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post("/store/test_store")
                response = client.post("/store/test_store")

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({"message": "A store with name 'test_store' already exists."},
                                     json.loads(response.data))

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                client.post("/store/test_store")
                self.assertIsNotNone(StoreModel.find_by_name("test_store"))

                response = client.delete("/store/test_store")
                self.assertEqual(response.status_code, 200)
                self.assertIsNone(StoreModel.find_by_name("test_store"))
                self.assertDictEqual({'message': 'Store deleted'}, json.loads(response.data))

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                client.post("/store/test_store")
                response = client.get("/store/test_store")

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({"name": "test_store", "items": []}, StoreModel.find_by_name("test_store").json())

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get("/store/test_store")

                self.assertEqual(response.status_code, 404)
                self.assertDictEqual({'message': 'Store not found'}, json.loads(response.data))

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                client.post("/store/test_store")
                item = ItemModel(name="test_item", price=1.99, store_id=1)
                item.save_to_db()
                response = client.get("/store/test_store")

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({"name": "test_store",
                                      "items": [
                                          {"name": "test_item",
                                           "price": 1.99
                                           }
                                      ]}, json.loads(response.data))

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                client.post("/store/test_store_1")
                client.post("/store/test_store_2")

                response = client.get("/stores")
                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(
                    {"stores": [
                        {"name": "test_store_1", "items": []},
                        {"name": "test_store_2", "items": []}
                    ]}, json.loads(response.data))

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                client.post("/store/test_store_1")
                item1 = ItemModel("test_name_1", 1.99, 1)
                item1.save_to_db()
                client.post("/store/test_store_2")

                response = client.get("/stores")
                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(
                    {"stores": [
                        {"name": "test_store_1", "items": [{"name": "test_name_1", "price": 1.99}]},
                        {"name": "test_store_2", "items": []}
                    ]}, json.loads(response.data))
