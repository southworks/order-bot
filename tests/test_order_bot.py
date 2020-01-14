from unittest import TestCase

import data_models


class TestOrderBot(TestCase):

    @staticmethod
    def test_adding_item():
        order = data_models.Order(0)
        item = data_models.Item(1, "Item1", 1)
        item.description = "item1"
        item.quantity = 1
        order.add_item(1, 0, item)

        assert item in order.item_list
