# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import enum

from data_models.item import Item


class Order:
    def __init__(self, order_id: int = 0, item_list: [Item] = []):
        self.order_id = order_id
        self.item_list = item_list

    def add_item(self, quantity, item):
        """ TODO: Add description for Order.add_item """
        return

    def remove_item(self, quantity, item):
        """ TODO: Add description for Order.remove_item """

        return

    def confirm_order(self):
        """ TODO: Add description for Order.confirm_order """

        return

    def to_string(self):
        """ returns a text representation of the object """
        # TODO: Implement method Order.to_string
        return "{0}".format(self.order_id)


class OrderStatus(enum.Enum):
    New = 0
    Pending = 1
    Confirmed = 2
