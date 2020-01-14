from botbuilder.core import StatePropertyAccessor, TurnContext
from botbuilder.dialogs import Dialog, DialogSet, DialogTurnStatus

from data_models import Add, Remove, Confirm, Item, Order


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
    def init_dialog():
        order_list = []
        # TODO: Move this Code to Tests
        # create units

        # create items
        item1 = Item(
            product_id=1,
            item_id=1,
            quantity=1,
            description="Coca Cola",
            unit='',
        )
        item2 = Item(
            product_id=2,
            item_id=2,
            quantity=3,
            description="Agua Mineral",
            unit='',
        )
        item3 = Item(
            product_id=3,
            item_id=3,
            weight=0.5,
            description="Frutos Secos",
            unit='Kg',
        )
        item4 = Item(
            product_id=4,
            item_id=4,
            quantity=5,
            description="Alfajor de Arroz",
            unit='',
        )
        item5 = Item(
            product_id=5,
            item_id=5,
            weight=0.5,
            description="Banana",
            unit='Kg',
        )
        item6 = Item(
            product_id=6,
            item_id=6,
            weight=0.5,
            description="Manzana",
            unit='Kg',
        )
        item7 = Item(
            product_id=7,
            item_id=7,
            weight=0.5,
            description="Yerba Organica",
            unit='Kg',
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
