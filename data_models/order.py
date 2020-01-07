import enum

from data_models.item import Item


class Order:
    def __init__(self, order_id: int = 0, item_list: [Item] = []):
        self.order_id = order_id
        self.item_list = item_list


class OrderStatus(enum.Enum):
    New = 0
    Pending = 1
    Confirmed = 2
