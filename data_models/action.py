from recognizers_text import Culture

from .item import Item


class Action:
    """ TODO: Add description for Action class. """

    def execute(self, quantity, weight, order, item):
        raise NotImplementedError

    @staticmethod
    def create_item(current_order, quantity, weight, item_description, unit):
        return Item(
            product_id=current_order.item_list[-1].product_id + 1,
            description=item_description,
            item_id=current_order.item_list[-1].item_id + 1,
            quantity=quantity,
            weight=weight,
            unit=unit
        )

    def parse_input(self, user_input, current_order):
        from helpers import DialogHelper

        results = [sub_list for sub_list in DialogHelper.parse_all(user_input, Culture.English) if sub_list]
        match = next((item for sublist in results for item in sublist), None)

        has_unit, weight, is_quantity, quantity, unit = DialogHelper.resolve_quantity_and_weigh(match)
        item_description = DialogHelper.normalize_description(has_unit, is_quantity, user_input, match)

        item = next(
            (
                x
                for x in current_order.item_list
                if x.description.lower() == item_description.lower()
            ),
            self.create_item(current_order, quantity, weight, item_description, unit),
        )

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

    def parse_input(self, user_input, current_order):
        return None, None, None, None, None, None, None

