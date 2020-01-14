from botbuilder.core import StatePropertyAccessor, TurnContext
from botbuilder.dialogs import Dialog, DialogSet, DialogTurnStatus

from data_models import Add, Remove, Confirm, Item, Order, Constants


class DialogHelper:
    @staticmethod
    async def run_dialog(
        dialog: Dialog,
        turn_context: TurnContext,
        accessor: StatePropertyAccessor,
    ):
        dialog_set = DialogSet(accessor)
        dialog_set.add(dialog)

        dialog_context = await dialog_set.create_context(turn_context)
        results = await dialog_context.continue_dialog()
        if results.status == DialogTurnStatus.Empty:
            await dialog_context.begin_dialog(dialog.id)

    @staticmethod
    def recognize_intention(text):
        if "add" in text:
            return Add()
        elif "remove" in text:
            return Remove()
        elif "confirm" in text:
            return Confirm()

    @staticmethod
    def normalize_description(has_unit, is_quantity, user_input, match):
        item_description = ''
        if has_unit:
            if 'of' in user_input:
                user_input = user_input.replace('of', '')
            item_description = user_input[match.start + len(match.text):].strip()
        elif is_quantity:
            user_input.strip()
            item_description = user_input[match.start + len(match.text):].strip()
        return item_description

    @staticmethod
    def resolve_quantity_and_weigh(match):
        is_quantity = False
        quantity = None
        weight = None
        has_unit = False
        type_name = match.type_name
        if type_name == Constants.number_type_name:
            if '.' in match.resolution.get('value'):
                has_unit = True
                weight = float(match.resolution.get('value'))
            else:
                is_quantity = True
                quantity = int(match.resolution.get('value'))
        elif type_name == Constants.dimension_type_name:
            has_unit = True
            weight = float(match.resolution.get('value'))
            unit = (match.resolution.get('unit'))

        return has_unit, weight, is_quantity, quantity, unit

    @staticmethod
    def init_dialog():
        order_list = []
        # TODO: Move this Code to Tests

        # create items
        item1 = Item(
            product_id=1,
            item_id=1,
            quantity=1,
            description="Coca Cola",
            unit="kg",
        )
        item2 = Item(
            product_id=2,
            item_id=2,
            quantity=3,
            description="Agua Mineral",
            unit="gr",
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

        order.add_item(item1.quantity, item1.weigth, item1)
        order.add_item(item2.quantity, item2.weigth, item2)
        order.add_item(item3.quantity, item3.weigth, item3)
        order.add_item(item3.quantity, item4.weigth, item4)
        order.add_item(item3.quantity, item5.weigth, item5)
        order.add_item(item3.quantity, item6.weigth, item6)
        order.add_item(item3.quantity, item7.weigth, item7)

        return order
