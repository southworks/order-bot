# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from orderbot.data_models.order import Order


class Action:
    """ TODO: Add description for Action class. """
    def execute(self, quantity, weight, order, item):
        raise NotImplementedError


class Add(Action):
    """ TODO: Add description for Add class. """
    def execute(self, quantity, weight, order: Order, item):
        order.add_item(quantity, weight, item)

    @property
    def description(self):
        return 'added'


class Remove(Action):
    """ TODO: Add description for Remove class. """
    def execute(self, quantity, weight, order: Order, item):
        order.remove_item(quantity,  weight, item)

    @property
    def description(self):
        return 'removed'


class Confirm(Action):
    """ TODO: Add description for Confirm class. """
    def execute(self, quantity, weight, order: Order, item):
        order.confirm_order()

    @property
    def description(self):
        return 'confirmed'
