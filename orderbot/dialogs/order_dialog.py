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

from orderbot.data_models import Order, Unit, Item


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
        unit = Unit(1)
        unit_kg = Unit(2, "Kg")

        # create item 1
        item1 = Item(product_id=1, item_id=1, quantity=5, description="Chocolate", unit=unit)

        # TODO: Use a better alternative to add known names
        # item1.known_names.append(item1.description)
        # item1.known_names.append("Coca 1.5")
        # item1.known_names.append("CC 1500")

        # create item 2
        item2 = Item(product_id=2, item_id=2, quantity=3, description="Yerba", unit=unit)

        # TODO: Use a better alternative to add known names
        # item2.known_names.append(item2.description)
        # item2.known_names.append("Yerba Mate")
        # item2.known_names.append("Yerba MarcaX")

        # create item 2
        item3 = Item(product_id=3, item_id=3, quantity=2, description="Candy", unit=unit)

        # create order
        order: Order = Order(1)

        if len(self.order_list) == 0:
            self.order_list.append(order)
            self.current_order = order

        # Add the item to the list:
        await step_context.context.send_activity(
            MessageFactory.text("Adding two items")
        )

        self.current_order.add_item(item1.quantity, item1)
        self.current_order.add_item(item2.quantity, item2)
        self.current_order.add_item(item3.quantity, item3)

        lista_estado_1 = "The items in the list are:\n" + self.current_order.show_items()
        # show list: 1 item
        await step_context.context.send_activity(
            MessageFactory.text(lista_estado_1)
        )
        print(lista_estado_1)

        await step_context.context.send_activity(
            MessageFactory.text("Now, we remove items from item1 and item2, and add a few to item3")
        )

        self.current_order.remove_item(2, item1)
        self.current_order.remove_item(2, item2)
        self.current_order.add_item(4, item3)

        # show list: should have less one item

        lista_estado_2 = "The items in the list are:\n" + self.current_order.show_items()

        print(lista_estado_2)
        # show list: 1 item

        await step_context.context.send_activity(
             MessageFactory.text(lista_estado_2)
        )

        # return await step_context.
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

