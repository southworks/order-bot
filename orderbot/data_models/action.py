# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from data_models import Order


class Action:
    """ TODO: Add description for Action class. """
    def execute(self, number, order, item):
        raise NotImplementedError


class Add(Action):
    """ TODO: Add description for Add class. """
    def execute(self, number, order: Order, item):
        order.add_item(number, item)


class Remove(Action):
    """ TODO: Add description for Remove class. """
    def execute(self, number, order: Order, item):
        order.remove_item(number, item)


class Confirm(Action):
    """ TODO: Add description for Confirm class. """
    def execute(self, number, order: Order, item):
        order.confirm_order()
