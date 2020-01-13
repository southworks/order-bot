

from .unit import Unit


class Item:
    """ Represents a generic item of an Order. """

    def __init__(
        self,
        product_id: int = 0,
        description: str = None,
        item_id: id = 0,
        known_names: str = None,
        quantity: float = 0,
        unit: Unit = None,
    ):
        self.product_id = product_id
        self.description = description
        self.item_id = item_id
        if not known_names:
            known_names = list()
        self.known_names = known_names
        self.quantity = quantity
        self.unit = unit

    def to_string(self) -> str:
        """ returns a text representation of the Item """
        # TODO: check if the description is ""
        if self.unit.description == "":
            return "{0} {1}".format(self.quantity, self.description)
        else:
            return "{0} {1} of {2}".format(
                self.quantity, self.unit.description, self.description
            )
