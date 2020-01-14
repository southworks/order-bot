from data_models import Order, Item
from unittest import TestCase


class TestOrderBot(TestCase):

    @staticmethod
    def test_adding_item():
        order = Order(0)
        item = Item(1, "Item1", 1)
        item.description = "item1"
        item.quantity = 1
        order.add_item(1, 0, item)

        assert item in order.item_list
