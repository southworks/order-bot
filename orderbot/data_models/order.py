# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import enum
from typing import List
from orderbot.data_models import Item


class Order:
    """ TODO: Add description for class Order """
    def __init__(self, order_id: int = 0):
        self.order_id = order_id
        self.item_list: List[Item] = list()
        self.status = OrderStatus.New

    # TODO: see if the parameter quantity is removed here
    def add_item(self, quantity: float, item: Item):
        """ Adds a new item or modifies one if is already present."""
        # is the item already in the list?

        item.quantity = quantity
        self.item_list.append(item)
        # TODO: Add return type
        return

    def remove_item(self, quantity, item):
        """ TODO: Add description for Order.remove_item """
        # TODO: Define the arithmetic, substitution or subtraction
        item.quantity = quantity
        self.item_list.remove(item)
        # TODO: Add return type
        return

    def confirm_order(self):
        """ TODO: Add description for Order.confirm_order """
        self.status = OrderStatus.Confirmed
        return

    def to_string(self):
        """ returns a text representation of the object """
        # TODO: Implement method Order.to_string
        return "{0}".format(self.order_id)

    def show_items(self) -> str:
        """ Returns the content of the list """
        content = ""
        if len(self.item_list) == 0:
            content += "The list is empty."
            return content

        for item in self.item_list:
            content += item.to_string() + "\n"

        return content


class OrderStatus(enum.Enum):
    New = 0
    InProgress = 1
    Confirmed = 2
