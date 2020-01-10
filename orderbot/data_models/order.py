# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import enum
from typing import List

from botbuilder.core import CardFactory
from botbuilder.schema import Attachment

import json

from orderbot.data_models.item import Item


class Order:
    """ Represents an Order, that contains a list of items to Order. """
    def __init__(self, order_id: int = 0):
        self.order_id = order_id
        self.item_list: List[Item] = list()
        self.status = OrderStatus.New

    def add_item(self, quantity: float, item: Item):
        """ Adds items to the list if there is no match
            Else, it updates the item.
        """
        if self.item_list:
            if item in self.item_list:
                for i in range(0, len(self.item_list)):
                    if item.product_id == self.item_list[i].product_id:
                        item.quantity += int(quantity) if item.unit.description == "" else quantity
                    else:
                        self.item_list.append(item)
            else:
                self.item_list.append(item)
        else:
            self.item_list.append(item)

    def remove_item(self, quantity, item):
        """ Removes items from the list if the remaining quantity is 0
            If quantity is greater than 0, then the item is modified
        """
        if quantity >= item.quantity:
            self.item_list.remove(item)
        else:
            item.quantity -= int(quantity) if item.unit.description == "" else quantity

    def confirm_order(self):
        """ Confirms the Order """
        self.status = OrderStatus.Confirmed
        return

    def to_string(self):
        """ returns a text representation of the object """
        # TODO: Implement method Order.to_string
        return "{0}".format(self.order_id)

    def show_items(self) -> str:
        """ Returns the content of the list """
        content = ""
        if len(self.item_list) == 0:
            content += "The list is empty."
            return content

        for item in self.item_list:
            content += item.to_string() + "\n"

        return content

    def get_table_style_card(self) -> Attachment:
        # parse through the list and show every element in a row
        # return CardFactory.adaptive_card(ADAPTIVE_CARD_CONTENT)
        PROTOTYPE_CARD_REAL = {
            "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
            "type": "AdaptiveCard",
            "version": "1.0",
            "body": [
                {
                    "type": "ColumnSet",
                    "columns": [
                        {
                            "type": "Column",
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "weight": "bolder",
                                    "text": "Quantity"
                                },
                                {
                                    "type": "TextBlock",
                                    "separator": True,
                                    "text": "5"
                                },
                                {
                                    "type": "TextBlock",
                                    "separator": False,
                                    "text": "3"
                                },
                                {
                                    "type": "TextBlock",
                                    "separator": False,
                                    "text": "2"
                                }
                            ]
                        },
                        {
                            "type": "Column",
                            "items": [
                                {
                                    "type": "TextBlock",
                                    "weight": "bolder",
                                    "text": "Item"
                                },
                                {
                                    "type": "TextBlock",
                                    "separator": True,
                                    "text": "Chocolate"
                                },
                                {
                                    "type": "TextBlock",
                                    "separator": False,
                                    "text": "Yerba"
                                },
                                {
                                    "type": "TextBlock",
                                    "separator": False,
                                    "text": "Candy"
                                }
                            ]
                        },
                    ]
                }
            ]
        }

        card = PROTOTYPE_CARD_REAL

        return Attachment(
            content_type=CardFactory.content_types.adaptive_card, content=card
        )

    # def create_table_style_card_2(self) -> Attachment:
    #     # card = Order.get_headers(self)
    #
    #     base_dict = {
    #         "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
    #         "type": "AdaptiveCard",
    #         "version": "1.0",
    #         "body": []
    #     }
    #
    #     # rare_card = '{\'$schema\': \'http://adaptivecards.io/schemas/adaptive-card.json\',\'type\': \'AdaptiveCard\',\'version\': \'1.0\'}'
    #     # resx = json.loads(card)
    #
    #     card += "'body': [{"
    #     card += "'type': 'ColumnSet',"
    #     card += "'columns': ["
    #
    #     card += Order.get_cells_quantity(self)
    #     card += Order.get_cells_description(self)
    #     card += Order.get_bottom(self)
    #     # card = card.replace("'", '"')
    #     # card = card.replace("True", 'true')
    #
    #     # printing original string
    #     print("The original string : " + str(card))
    #
    #     # using json.loads()
    #     # convert dictionary string to dictionary
    #     res = json.loads(card)
    #
    #     return Attachment(
    #         content_type=CardFactory.content_types.adaptive_card, content=res
    #     )

    def get_headers(self) -> str:
        rows_text: str = ""
        rows_text += "{"

        rows_text += "'$schema': 'http://adaptivecards.io/schemas/adaptive-card.json',"
        rows_text += "'type': 'AdaptiveCard',"
        rows_text += "'version': '1.0',"
        rows_text = rows_text.rstrip(',')

        # rows_text += "'body': [{"
        # rows_text += "'type': 'ColumnSet',"
        # rows_text += "'columns': ["
        return rows_text

    def get_cells_quantity(self) -> str:
        rows_text: str = ""

        rows_text += "{"
        rows_text += "'type': 'Column', 'items': ["

        # header
        rows_text += "{"
        rows_text += "'type': 'TextBlock', 'separator': True, 'text': '{0}'".format("Quantity")
        rows_text += "},"

        for item in self.item_list:
            rows_text += "{"
            rows_text += "'type': 'TextBlock', 'separator': False, 'text': '{0}'".format(str(item.quantity))
            rows_text += "},"

        # remove last trailing comma
        rows_text = rows_text.rstrip(',')
        rows_text += "]}"
        rows_text += ","

        return rows_text

    def get_cells_description(self) -> str:
        rows_text: str = ""

        rows_text += "{"
        rows_text += "'type': 'Column', 'items': ["

        # header
        rows_text += "{"
        rows_text += "'type': 'TextBlock', 'separator': False, 'text': '{0}'".format("Item")
        rows_text += "},"

        for item in self.item_list:
            rows_text += "{"
            rows_text += "'type': 'TextBlock', 'separator': True, 'text': '{0}'".format(item.description)
            rows_text += "},"

        # remove last trailing comma
        rows_text = rows_text.rstrip(',')
        rows_text += "]}"

        return rows_text

    def get_bottom(self) -> str:
        rows_text: str = ""
        rows_text += "]}]}"
        return rows_text


class OrderStatus(enum.Enum):
    New = 0
    InProgress = 1
    Confirmed = 2
