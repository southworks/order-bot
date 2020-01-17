import recognizers_suite
from botbuilder.core import StatePropertyAccessor, TurnContext
from botbuilder.dialogs import Dialog, DialogSet, DialogTurnStatus

from data_models import Add, Remove, Confirm, Item, Order, Constants


class DialogHelper:

    @staticmethod
    def recognize_intention(text):
        if "add" in text:
            return Add()
        elif "remove" in text:
            return Remove()
        elif "confirm" in text:
            return Confirm()

    @staticmethod
    def normalize_description(has_unit, is_quantity, user_input, unit, match):
        splitted_input = user_input.split()
        item_description = ''
        if has_unit:
            if 'of' in user_input:
                user_input = user_input.replace('of', '')
            item_description = user_input[match.end + len(match.text) + len(unit):].strip()
        elif is_quantity:
            user_input.strip()
            item_description = user_input[match.end + len(match.text):].strip()
        else:
            item_description = user_input[len(splitted_input[0]):].strip()
        return item_description

    @staticmethod
    def resolve_quantity_and_weight(match):
        is_quantity = False
        quantity = 0
        weight = 0
        has_unit = False
        type_name = match.type_name if match else ''

        if type_name == Constants.number_type_name:
            if '.' in match.resolution.get('value'):
                has_unit = True
                quantity = 0
                weight = float(match.resolution.get('value'))
            else:
                is_quantity = True
                weight = 0
                quantity = int(match.resolution.get('value'))
        elif type_name == Constants.dimension_type_name:
            has_unit = True
            weight = float(match.resolution.get('value'))
            quantity = 0

        return has_unit, weight, is_quantity, quantity

    @staticmethod
    def init_dialog():
        order_list = []

        # create items
        item1 = Item(
            product_id=1,
            item_id=1,
            quantity=1,
            description="Coca Cola",
        )
        item2 = Item(
            product_id=2,
            item_id=2,
            quantity=3,
            description="Agua Mineral",
        )
        item3 = Item(
            product_id=3,
            item_id=3,
            weight=0.5,
            description="Frutos Secos",
            unit="kg",
        )
        item4 = Item(
            product_id=4,
            item_id=4,
            quantity=5,
            description="Alfajor de Arroz",
        )
        item5 = Item(
            product_id=5,
            item_id=5,
            weight=0.5,
            description="Banana",
            unit="kg",
        )
        item6 = Item(
            product_id=6,
            item_id=6,
            weight=0.5,
            description="Manzana",
            unit="kg",
        )
        item7 = Item(
            product_id=7,
            item_id=7,
            weight=0.5,
            description="Yerba Organica",
            unit="kg",
        )

        # create order
        order: Order = Order(1)

        if len(order_list) == 0:
            order_list.append(order)
            order = order

        order.item_list.clear()

        # order.add_item(item1.quantity, item1.weight, item1)
        # order.add_item(item2.quantity, item2.weight, item2)
        # ...
        # order.add_item(item3.quantity, item7.weight, item7)

        order.read_json_data_from_file()

        return order

    @staticmethod
    def parse_all(user_input: str, culture: str):
        return [
            # Number recognizer - This function will find any number from the input
            # E.g "I have two apples" will return "2".
            recognizers_suite.recognize_number(user_input, culture),

            # Dimension recognizer - This function will find any dimension presented E.g "The six-mile trip to my airport
            # hotel that had taken 20 minutes earlier in the day took more than
            # three hours." will return "6 Mile"
            recognizers_suite.recognize_dimension(user_input, culture),

        ]