from unittest import TestCase
from models.item import ItemModel
from tests.unit.unit_base_test import UnitBaseTest


class ItemTest(TestCase):
    def setUp(self):
        item = ItemModel('Test Name', 1.82, 1)

    def test_create_item(self):
        item = ItemModel('Test Name', 1.82, 1)
        self.assertEqual(item.name, "Test Name",
                         "The name of the item does not equal the constructor argument")
        self.assertEqual(item.price, 1.82,
                         "The price of the item does not equal the constructor argument")

    def test_json(self):
        item = ItemModel('Test Name', 1.82, 1)
        expected = {
            "name": "Test Name",
            "price": 1.82,
        }
        self.assertEqual(expected, item.json(),
                         f"The JSON function of the item object is incorrect. Received {item.json()}, expected {expected}.")
