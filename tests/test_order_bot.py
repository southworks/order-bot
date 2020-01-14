from data_models import Order, Item


class TestOrderBot:
    @staticmethod
    def test_adding_item():
        order = Order(0)
        item = Item(1, "Item1", 1)
        item.description = "item1"
        item.quantity = 1
        order.add_item(1, 0, item)
