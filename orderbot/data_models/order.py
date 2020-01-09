# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import enum
from typing import List
from orderbot.data_models import Item


class Order:
    """ Represents an Order, that contains a list of items to Order. """
    def __init__(self, order_id: int = 0):
        self.order_id = order_id
        self.item_list: List[Item] = list()
        self.status = OrderStatus.New

    def add_item(self, quantity: float, item: Item):
        """ Adds items to the list if there is no match
            Else, it updates the item.
        """
        if item in self.item_list:
            item.quantity += int(quantity) if item.unit.description == "" else quantity
        else:
            self.item_list.append(item)

    def remove_item(self, quantity, item):
        """ Removes items from the list if the remaining quantity is 0
            If quantity is greater than 0, then the item is modified
        """
        if quantity >= item.quantity:
            self.item_list.remove(item)
        else:
            item.quantity -= int(quantity) if item.unit.description == "" else quantity

    def confirm_order(self):
        """ Confirms the Order """
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
