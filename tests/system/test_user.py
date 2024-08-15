from models.user import UserModel
from tests.base_test import BaseTest
import json
from flask import jsonify


class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as client:
            with self.app_context():
                response = client.post("/register",
                                       data=json.dumps({"username": "Test Username",
                                                        "password": "Test Password"}),
                                       headers={"Content-Type": "application/json"})
                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username("Test Username"))
                self.assertDictEqual({"message": "User created successfully."}, json.loads(response.data))

    def test_register_and_login(self):
        with self.app() as client:
            with self.app_context():
                client.post("/register",
                            data=json.dumps({"username": "Test Username",
                                             "password": "Test Password"}),
                            headers={"Content-Type": "application/json"})
                auth_request = client.post("/auth",
                                           data=json.dumps({"username": "Test Username",
                                                            "password": "Test Password"}),
                                           headers={"Content-Type": "application/json"})

                self.assertIn('access_token', json.loads(auth_request.data).keys())

    def test_register_duplicate_user(self):
        with self.app() as client:
            with self.app_context():
                client.post("/register",
                            data=json.dumps({"username": "Test Username",
                                             "password": "Test Password"}),
                            headers={"Content-Type": "application/json"})
                response = client.post("/register",
                                       data=json.dumps({"username": "Test Username",
                                                        "password": "Test Password"}),
                                       headers={"Content-Type": "application/json"})

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({"message": "Error: A user with that name already exists."}, json.loads(response.data))