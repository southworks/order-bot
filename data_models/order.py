import enum
from typing import List

from botbuilder.core import CardFactory
from botbuilder.schema import Attachment
from datetime import datetime
from pyadaptivecards.card import AdaptiveCard
from pyadaptivecards.components import TextBlock, Column
from pyadaptivecards.container import ColumnSet

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
                        item.quantity += 0 if not quantity else quantity
                        item.weigth += 0 if not weight else weight
            else:
                self.item_list.append(item)
        else:
            self.item_list.append(item)

    def remove_item(self, quantity, weight, item):
        """ Removes items from the list if the remaining quantity is 0
            If quantity is greater than 0, then the item is modified
        """
        if (quantity and quantity != 0 and quantity >= item.quantity) or (weight and weight != 0 and weight >= item.weigth):
            self.item_list.remove(item)
        elif not item.unit and quantity != 0:
            item.quantity -= quantity
        elif not item.unit and weight != 0:
            item.weigth -= weight

    def confirm_order(self):
        ''' Confirms the Order '''
        self.status = OrderStatus.Confirmed
        return

    def to_string(self):
        ''' returns a text representation of the object '''
        return '{0}'.format(self.order_id)

    def show_items(self) -> str:
        ''' Returns the content of the list '''
        content = ''
        if len(self.item_list) == 0:
            content += 'The list is empty.'
            return content

        content += 'The items in the order are:\n'
        for item in self.item_list:
            content += item.to_string() + '\n'

        return content

    def generate_list_items_card(self) -> Attachment:
        from pyadaptivecards.card import AdaptiveCard
        from pyadaptivecards.components import TextBlock
        from pyadaptivecards.actions import Submit, OpenUrl, ShowCard
        
        order_number = '001'
        body = []
        greeting = TextBlock(f'Order #{order_number}', weight='bolder', size='medium')
        submit = Submit(title='Confirm Order')
        date = TextBlock(str(datetime.now().strftime('%a. %d of %b, %Y at %H:%M')), size='small')
        body.append(greeting)
        body.append(date)

        quantity_column_items = [TextBlock('Quantity', weight='bolder')]
        item_column_items = [TextBlock('Item', weight='bolder')]

        for item in self.item_list:

            if item.unit == '' or item.quantity != 0:
                item_column_items.append(TextBlock(f'{item.description.capitalize()}'))
                quantity_column_items.append(TextBlock(f'{item.quantity}'))
            else:
                item_column_items.append(TextBlock(f'{item.description.capitalize()}'))
                quantity_column_items.append(TextBlock(f'{item.weigth} {item.unit.capitalize()}'))

        card = AdaptiveCard(body=body, actions=[submit])
        quantity_column = Column(items=quantity_column_items)
        item_column = Column(items=item_column_items)
        table = ColumnSet(columns=[quantity_column, item_column])
        body.append(table)
        # Create attachment
        attachment = {
            'contentType': 'application/vnd.microsoft.card.adaptive',
            'content': card.to_dict()
        }
        data_value = attachment['content']['actions'][0]['data'] = 'Confirm'

        return attachment


class OrderStatus(enum.Enum):
    New = 0
    InProgress = 1
    Confirmed = 2
