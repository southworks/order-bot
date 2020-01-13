from typing import List

from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs.prompts import (
    TextPrompt,
    ChoicePrompt,
    ConfirmPrompt,
    PromptOptions,
)
from botbuilder.core import MessageFactory, UserState

from helpers import DialogHelper
from data_models import Unit, Item, Order, OrderStatus

from helpers import activity_helper


class OrderDialog(ComponentDialog):
    """ TODO: Add description for OrderDialog class. """

    def __init__(self, user_state: UserState):
        super(OrderDialog, self).__init__(OrderDialog.__name__)
        self.current_order: Order = None
        self.order_list: List[Order] = list()
        self.user_profile_accesor = user_state.create_property("UserProfile")

        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [
                    self.options_step,
                    self.interpret_user_intention,
                    self.goodbye_step,
                ],
            )
        )
        self.add_dialog(ChoicePrompt("options_step"))
        self.add_dialog(TextPrompt("interpret_user_intention"))
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.initial_dialog_id = WaterfallDialog.__name__
        self.add_dialog(TextPrompt(TextPrompt.__name__))

    async def options_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        if not step_context.options:
            # TODO: Move this Code to Tests
            # create units
            unit = Unit(1)
            unit_gr = Unit(2, "Gr")
            unit_kg = Unit(3, "Kg")

            # create items
            item1 = Item(
                product_id=1,
                item_id=1,
                quantity=1,
                description="Coca Cola",
                unit=unit,
            )
            item2 = Item(
                product_id=2,
                item_id=2,
                quantity=3,
                description="Agua Mineral",
                unit=unit,
            )
            item3 = Item(
                product_id=3,
                item_id=3,
                weight=500,
                description="Frutos Secos",
                unit=unit_gr,
            )
            item4 = Item(
                product_id=4,
                item_id=4,
                quantity=5,
                description="Alfajor de Arroz",
                unit=unit,
            )
            item5 = Item(
                product_id=5,
                item_id=5,
                weight=500,
                description="Banana",
                unit=unit_gr,
            )
            item6 = Item(
                product_id=6,
                item_id=6,
                weight=500,
                description="Manzana",
                unit=unit_gr,
            )
            item7 = Item(
                product_id=7,
                item_id=7,
                weight=500,
                description="Yerba Organica",
                unit=unit_gr,
            )

            # create order
            order: Order = Order(1)

            if len(self.order_list) == 0:
                self.order_list.append(order)
                self.current_order = order

            self.current_order.item_list.clear()

            self.current_order.add_item(item1.quantity, item1.weigth, item1)
            self.current_order.add_item(item2.quantity, item2.weigth, item2)
            self.current_order.add_item(item3.quantity, item3.weigth, item3)
            self.current_order.add_item(item3.quantity, item4.weigth, item4)
            self.current_order.add_item(item3.quantity, item5.weigth, item5)
            self.current_order.add_item(item3.quantity, item6.weigth, item6)
            self.current_order.add_item(item3.quantity, item7.weigth, item7)

        card = self.current_order.generate_list_items_card()

        response = activity_helper.create_activity_reply(
            step_context.context.activity, "", "", [card]
        )

        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=response)
        )

    async def interpret_user_intention(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """
            New step that interprets the user intent, using a split and invoking add and remove
        """
        unit = Unit(1)
        step_context.values["input"] = step_context.result
        query = str(step_context.result).lower()
        splitted = query.split()

        action = DialogHelper.recognize_intention(query)

        if len(splitted) > 1:
            item_description = query[
                query.find((splitted[2])[0]):
            ].capitalize()
        else:
            item_description = splitted[0]

        item = next(
            (
                x
                for x in self.current_order.item_list
                if x.description.lower() == item_description.lower()
            ),
            None,
        )

        is_item = True if item else False

        item_quantity = int(splitted[1]) if is_item and item.weigth == 0 else 0
        item_weight = int(splitted[1]) if is_item and item.quantity == 0 else 0
        if not item and action.description != "confirmed":
            item = Item(
                product_id=self.current_order.item_list[-1].product_id + 1,
                description=item_description,
                item_id=self.current_order.item_list[-1].item_id + 1,
                quantity=int(splitted[1]),
                unit=unit,
            )
            item_quantity = item.quantity
            item_weight = item.weigth

        action.execute(item_quantity, item_weight, self.current_order, item)

        if self.current_order.status == OrderStatus.Confirmed:
            if (
                type(step_context.result) is bool and not step_context.result
            ) or (
                type(step_context.result) is str
                and not "confirm" in step_context.result.lower()
            ):
                prompt_message = MessageFactory.text(
                    "I don't want to do that right now"
                )
                await step_context.prompt(
                    TextPrompt.__name__, PromptOptions(prompt=prompt_message)
                )

                return await step_context.end_dialog()
            elif (
                type(step_context.result) is bool and step_context.result
            ) or (
                type(step_context.result) is str
                and "confirm" in step_context.result.lower()
            ):
                return await step_context.prompt(
                    ConfirmPrompt.__name__,
                    PromptOptions(
                        prompt=MessageFactory.text(
                            "You want to confirm this order?"
                        )
                    ),
                )
        await step_context.context.send_activity(
            MessageFactory.text(
                f"{splitted[1]} {item_description} was {action.description}!"
            )
        )
        return await step_context.replace_dialog(self.id, step_context.result)

    async def goodbye_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """ TODO: Add description for OrderDialog.second_step """
        if step_context.result:
            await step_context.context.send_activity(
                MessageFactory.text("The order was confirmed!")
            )
            await step_context.context.send_activity(MessageFactory.text("Thank you!"))

            await step_context.context.send_activity(
                MessageFactory.text("Bye!")
            )

            return await step_context.end_dialog()
        else:
            return await step_context.replace_dialog(
                self.id, step_context.result
            )
