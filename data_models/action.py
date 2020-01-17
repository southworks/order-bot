from recognizers_text import Culture

from data import constants
from .item import Item


class Action:
    """ TODO: Add description for Action class. """

    def execute(self, quantity, weight, order, item):
        raise NotImplementedError

    @staticmethod
    def create_item(current_order, quantity, weight, item_description, unit):
        try:
            new_product_id: int = int(current_order.item_list[-1].product_id) + 1
            new_item_id: int = int(current_order.item_list[-1].item_id) + 1
        except ValueError:
            print('product_id NaN')
            new_product_id = -1
            new_item_id = -1

        return Item(
            product_id=new_product_id,
            description=item_description,
            item_id=new_item_id,
            quantity=quantity,
            weight=weight,
            unit=unit
        )

    def parse_input(self, user_input, current_order, action):
        from helpers import DialogHelper

        splitted_input = user_input.split()
        unit = ''
        for input in splitted_input:
            if input in constants.ConstantUnits.units:
                has_unit = True
                unit = input

        results = [sub_list for sub_list in DialogHelper.parse_all(user_input, Culture.English) if sub_list]
        match = next((item for sublist in results for item in sublist), None)

        has_unit, weight, is_quantity, quantity = DialogHelper.resolve_quantity_and_weight(match)
        item_description = DialogHelper.normalize_description(has_unit, is_quantity, user_input, unit, match)

        item = next(
            (
                x
                for x in current_order.item_list
                if x.description.lower() == item_description.lower()
            ),
            self.create_item(current_order, quantity, weight, item_description, unit),
        )

        if action.description == 'added':
            if weight == 0 and item.unit != '':
                weight = 0.5
            elif quantity == 0 and item.unit == '':
                quantity = 1
        else:
            if weight == 0 and item.unit != '':
                weight = item.weight
            elif quantity == 0 and item.unit == '':
                quantity = item.quantity

        return has_unit, weight, is_quantity, quantity, unit, item_description, item


class Add(Action):
    """ TODO: Add description for Add class. """

    def execute(self, quantity, weight, order, item):
        order.add_item(quantity, weight, item)

    @property
    def description(self):
        return "added"


class Remove(Action):
    """ TODO: Add description for Remove class. """

    def execute(self, quantity, weight, order, item):
        order.remove_item(quantity, weight, item)

    @property
    def description(self):
        return "removed"


class Confirm(Action):
    """ TODO: Add description for Confirm class. """

    def execute(self, quantity, weight, order, item):
        order.confirm_order()

    @property
    def description(self):
        return "confirmed"

    @staticmethod
    def create_item(current_order, quantity, weight, item_description, unit):
        return None

    def parse_input(self, user_input, current_order, action):
        return None, None, None, None, None, None, None

