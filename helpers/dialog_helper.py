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
        order: Order = Order(1)
        order.item_list.clear()
        order.read_json_data_from_file()

        return order

    @staticmethod
    def parse_all(user_input: str, culture: str):
        return [
            recognizers_suite.recognize_number(user_input, culture),
            recognizers_suite.recognize_dimension(user_input, culture),

        ]
