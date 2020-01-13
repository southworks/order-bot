class Action:
    """ TODO: Add description for Action class. """

    def execute(self, quantity, weight, order, item):
        raise NotImplementedError


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
