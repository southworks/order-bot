from data_models import Order
from dialogs import OrderDialog


class TestOrderBot:

    @staticmethod
    def test_dummy_test():
        order = Order(0)
        order.add_item()
