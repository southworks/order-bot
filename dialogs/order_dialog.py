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
from orderbot.helpers.activity_helper import create_activity_reply


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
                    self.third_step

                ],
            )
        )
        self.add_dialog(ChoicePrompt("options_step"))
        self.add_dialog(TextPrompt("interpret_user_intention"))
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.initial_dialog_id = WaterfallDialog.__name__
        self.add_dialog(TextPrompt(TextPrompt.__name__))

    async def options_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        # TODO: Move this Code to Tests
        # create units
        unit = Unit(1)
        unit_kg = Unit(2, "Kg")

        # create items
        item1 = Item(product_id=1, item_id=1, quantity=5, description="Chocolate", unit=unit)
        item2 = Item(product_id=2, item_id=2, quantity=3, description="Yerba", unit=unit)
        item3 = Item(product_id=3, item_id=3, quantity=2, description="Candy", unit=unit)

        # create order
        order: Order = Order(1)

        if len(self.order_list) == 0:
            self.order_list.append(order)
            self.current_order = order

        self.current_order.item_list.clear()

        self.current_order.add_item(item1.quantity, item1)
        self.current_order.add_item(item2.quantity, item2)
        self.current_order.add_item(item3.quantity, item3)

        await step_context.context.send_activity(
            MessageFactory.text("You can Remove or Add an item to the list (Remove/Add 1 item)")
        )

        await step_context.context.send_activity(
            MessageFactory.text("When you are ready to confirm the order, type 'Confirm order'")
        )

        lista_estado = "The items in the list are:\n" + self.current_order.show_items()

        prompt_message = MessageFactory.text(
            lista_estado
        )

        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=prompt_message)
        )

    async def interpret_user_intention(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """
            New step that interprets the user intent, using a split and invoking add and remove
        """
        step_context.values["input"] = step_context.result
        query = str(step_context.result).lower()

        if "confirm" not in query:
            splitted = query.split()
            unit = Unit(1)

            item = next((x for x in self.current_order.item_list if x.description.lower() == splitted[2].lower()), None)
            if not item:
                item = Item(product_id=self.current_order.item_list[-1].product_id + 1, description=splitted[2],
                            item_id=self.current_order.item_list[-1].item_id + 1, quantity=int(splitted[1]), unit=unit)
            if "add" in query:
                self.current_order.add_item(float(splitted[1]), item)
                await step_context.context.send_activity(
                    MessageFactory.text(splitted[1] + " " + splitted[2] + " added!")
                )
            elif "remove" in query:
                self.current_order.remove_item(float(splitted[1]), item)
                await step_context.context.send_activity(
                    MessageFactory.text(splitted[1] + " " + splitted[2] + " removed!")
                )

            lista_estado_3 = "The items in the list are:\n" + self.current_order.show_items()
            # ------------------------------------------------
            # card = Order.get_table_style_card(self.current_order)
            #
            # response = create_activity_reply(
            #     step_context.context.activity, "", "", [card]
            # )
            # await step_context.context.send_activity(response)
            # ------------------------------------------------

            prompt_message = MessageFactory.text(lista_estado_3)
            return await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )
            # TODO: test this
            # return await self.interpret_user_intention(step_context)

        else:
            return await step_context.prompt(
                ConfirmPrompt.__name__,
                PromptOptions(prompt=MessageFactory.text("You want to confirm this order?")),
            )

    async def third_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """ TODO: Add description for OrderDialog.second_step """
        if "confirm" not in step_context.result.lower():
            prompt_message = MessageFactory.text("I don't want to do that right now")
            await step_context.prompt(
                TextPrompt.__name__, PromptOptions(prompt=prompt_message)
            )

            return await step_context.end_dialog()
            # TODO: Fix here, see something alternative
            # await self.interpret_user_intention(step_context)
        elif 'confirm' in step_context.result.lower():
            await step_context.context.send_activity(
                MessageFactory.text("The order was confirmed!")
            )
            await step_context.context.send_activity(
                MessageFactory.text("Thank you!")
            )

        await step_context.context.send_activity(
            MessageFactory.text("Bye!")
        )

        return await step_context.end_dialog()