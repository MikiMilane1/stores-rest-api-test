from models.item import ItemModel
from models.user import UserModel
from models.store import StoreModel
from tests.base_test import BaseTest

import json


class ItemTest(BaseTest):
    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                ItemModel("test_item", 1.99, 1)
                response = client.get("/item/test_item")

                self.assertEqual(response.status_code, 401)
                self.assertDictEqual(
                    {"description": "Request does not contain an access token", "error": "authorization_required"},
                    json.loads(response.data))

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                UserModel("test_user", "test_password").save_to_db()
                auth_request = client.post("/auth",
                                           data=json.dumps({"username": "test_user", "password": "test_password"}),
                                           headers={"Content-Type": "application/json"})
                auth_token = json.loads(auth_request.data)["access_token"]
                header = {"Authorization": f"Bearer {auth_token}"}
        pass

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                UserModel("test_user", "test_password").save_to_db()
                auth_request = client.post("/auth",
                                           data=json.dumps({"username": "test_user", "password": "test_password"}),
                                           headers={"Content-Type": "application/json"})
                auth_token = json.loads(auth_request.data)["access_token"]
                header = {"Authorization": f"Bearer {auth_token}"}

                ItemModel("test_item", 1.99, 1).save_to_db()
                response = client.get("/item/test_item", headers=header)
                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({"name": "test_item", "price": 1.99}, json.loads(response.data))

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test_store").save_to_db()
                response = client.post("/item/test_item",
                                       data=json.dumps({"price": 1.99, "store_id": 1}),
                                       headers={"Content-Type": "application/json"})

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(ItemModel.find_by_name("test_item"))
                self.assertDictEqual({"name": "test_item", "price": 1.99}, json.loads(response.data))

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test_store").save_to_db()
                ItemModel("test_item", 19.9, 1).save_to_db()

                response = client.delete("/item/test_item")
                self.assertEqual(response.status_code, 200)
                self.assertIsNone(ItemModel.find_by_name("test_item"))
                self.assertDictEqual({'message': 'Item deleted'}, json.loads(response.data))

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test_store").save_to_db()
                ItemModel("test_item", 19.9, 1).save_to_db()

                response = client.post("/item/test_item",
                                       data=json.dumps({"price": 1.99, "store_id": 1}),
                                       headers={"Content-Type": "application/json"})

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': "An item with name 'test_item' already exists."}, json.loads(response.data))

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test_store").save_to_db()
                response = client.put("/item/test_item",
                                      data=json.dumps({"price": 1.99, "store_id": 1}),
                                      headers={"Content-Type": "application/json"})

                self.assertEqual(response.status_code, 200)
                self.assertEqual(ItemModel.find_by_name("test_item").price, 1.99)
                self.assertDictEqual({"name": "test_item", "price": 1.99}, json.loads(response.data))

    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test_store").save_to_db()
                ItemModel("test_item", 1.99, 1)
                response = client.put("/item/test_item",
                                      data=json.dumps({"price": 1.29, "store_id": 1}),
                                      headers={"Content-Type": "application/json"})

                self.assertEqual(response.status_code, 200)
                self.assertEqual(ItemModel.find_by_name("test_item").price, 1.29)
                self.assertDictEqual({"name": "test_item", "price": 1.29}, json.loads(response.data))

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel("test_store").save_to_db()
                ItemModel("test_item_1", 1.99, 1).save_to_db()
                ItemModel("test_item_2", 1.99, 1).save_to_db()

                response = client.get("/items")
                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({"items": [
                    {
                        "name": "test_item_1",
                        "price": 1.99,
                    },
                    {
                        "name": "test_item_2",
                        "price": 1.99,
                    }
                ]}, json.loads(response.data))
