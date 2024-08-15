from models.user import UserModel
from tests.unit.unit_base_test import UnitBaseTest

class UnitTest(UnitBaseTest):
    def test_create_user(self):
        user = UserModel("Test Username", "Test Password")

        self.assertEqual(user.username, "Test Username")
        self.assertEqual(user.password, "Test Password")