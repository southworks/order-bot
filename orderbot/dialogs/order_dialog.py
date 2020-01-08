# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from typing import List

from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs.prompts import (
    TextPrompt,
    NumberPrompt,
    ChoicePrompt,
    ConfirmPrompt,
    PromptOptions,
    PromptValidatorContext,
)
from botbuilder.dialogs.choices import Choice
from botbuilder.core import MessageFactory, UserState

from data_models.order import Order
from data_models.item import Item
from data_models.unit import Unit


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
                    self.second_step
                ],
            )
        )
        self.add_dialog(ChoicePrompt("options_step"))

        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.initial_dialog_id = WaterfallDialog.__name__

    async def options_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:

        # testing 1
        # TODO: Move this Code to Tests
        # create unit
        unit = Unit(1, "Unit")
        unit_kg = Unit(2, "Kg")

        # create item 1
        item1 = Item(product_id=1, item_id=1, quantity=1, description="Producto1", unit=unit)

        # TODO: Use a better alternative to add known names
        item1.known_names.append("Producto1")
        item1.known_names.append("Producto 1")
        item1.known_names.append("Prod 1")

        # create item 2
        item2 = Item(product_id=2, item_id=2, quantity=1, description="Producto2", unit=unit_kg)

        # TODO: Use a better alternative to add known names
        item2.known_names.append("Producto2")
        item2.known_names.append("Producto 2")
        item2.known_names.append("Prod 2")

        # create order
        order: Order = Order(1)

        if len(self.order_list) == 0:
            self.order_list.append(order)
            self.current_order = order

        # Add the item to the list:
        self.current_order.add_item(item1.quantity, item1)
        self.current_order.add_item(item2.quantity, item2)

        # show list: 1 item
        print(order.show_items())

        self.current_order.remove_item(item1.quantity, item1)

        # show list: should have less one item
        print(order.show_items())

        return await step_context.prompt(
            ChoicePrompt.__name__,
            PromptOptions(
                prompt=MessageFactory.text("Welcome! What can I help you with?"),
                choices=[Choice("Add"), Choice("Remove"), Choice("Help")],
            ),
        )

    async def second_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """ TODO: Add description for OrderDialog.second_step """
        return_response = "Bye!"

        await step_context.context.send_activity(
            MessageFactory.text(return_response)
        )

        return await step_context.end_dialog()

