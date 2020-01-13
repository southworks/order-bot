import enum
from typing import List

from botbuilder.core import CardFactory
from botbuilder.schema import Attachment
from pyadaptivecards.card import AdaptiveCard
from pyadaptivecards.components import TextBlock

from .item import Item


class Order:
    """ Represents an Order, that contains a list of items to Order. """

    def __init__(self, order_id: int = 0):
        self.order_id = order_id
        self.item_list: List[Item] = list()
        self.status = OrderStatus.New

    def add_item(self, quantity: int, weight: float, item: Item):
        """ Adds items to the list if there is no match
            Else, it updates the item.
        """
        if self.item_list:
            if item in self.item_list:
                for i in range(0, len(self.item_list)):
                    if item.product_id == self.item_list[i].product_id:
                        item.quantity += quantity
                        item.weigth += weight
            else:
                self.item_list.append(item)
        else:
            self.item_list.append(item)

    def remove_item(self, quantity, weight, item):
        """ Removes items from the list if the remaining quantity is 0
            If quantity is greater than 0, then the item is modified
        """
        if (
            quantity != 0
            and quantity >= item.quantity
            or weight >= item.weigth
        ):
            self.item_list.remove(item)
        elif item.unit.description != "" and quantity != 0:
            item.quantity -= quantity
        elif item.unit.description != "" and weight != 0:
            item.weigth -= weight

    def confirm_order(self):
        """ Confirms the Order """
        self.status = OrderStatus.Confirmed
        return

    def to_string(self):
        """ returns a text representation of the object """
        return "{0}".format(self.order_id)

    def show_items(self) -> str:
        """ Returns the content of the list """
        content = ""
        if len(self.item_list) == 0:
            content += "The list is empty."
            return content

        content += "The items in the order are:\n"
        for item in self.item_list:
            content += item.to_string() + "\n"

        return content

    def generate_list_items_card(self) -> Attachment:
        from pyadaptivecards.card import AdaptiveCard
        from pyadaptivecards.inputs import Text, Number
        from pyadaptivecards.components import TextBlock
        from pyadaptivecards.actions import Submit

        body = []
        greeting = TextBlock("Current order", color="good", weight="bolder", size="medium")
        submit = Submit(title="Confirm Order")

        body.append(greeting)

        for item in self.item_list:
            item_desc = TextBlock(str(item.quantity) + " " + item.description)
            body.append(item_desc)

        # card = AdaptiveCard(body=body, actions=[submit])
        card = AdaptiveCard(body=body, actions=[submit])

        # Create attachment
        attachment = {
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": card.to_dict()
        }

        return attachment


class OrderStatus(enum.Enum):
    New = 0
    InProgress = 1
    Confirmed = 2
