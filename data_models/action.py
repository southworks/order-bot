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
            unit= unit
        )

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

    def create_item(self, quantity, weight, item_description):
        return None
