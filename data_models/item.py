

class Item:
    """ Represents a generic item of an Order. """

    def __init__(
        self,
        product_id: int = 0,
        description: str = None,
        item_id: id = 0,
        known_names: str = None,
        quantity: float = 0,
        weight: float = 0,
        unit='',
    ):
        self.product_id = product_id
        self.description = description
        self.item_id = item_id
        if not known_names:
            known_names = list()
        self.known_names = known_names
        self.quantity = quantity
        self.unit = unit
        self.weight = weight

    def to_string(self) -> str:
        """ returns a text representation of the Item """
        if self.unit == '':
            return f'{self.quantity} {self.description.capitalize()}'
        elif self.unit != '' and self.quantity == 0:
            return f'{self.weight} {self.unit} of {self.description.capitalize()}'
        elif (
                self.unit != ''
                and self.quantity != 0
                and self.weight != 0
        ):
            return f'{self.quantity} {self.description.capitalize()} of {self.weight}{self.unit}'
