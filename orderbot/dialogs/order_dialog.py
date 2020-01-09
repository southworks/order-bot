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
                    self.interpret_user_intention,
                    self.third_step
                ],
            )
        )
        self.add_dialog(ChoicePrompt("options_step"))
        self.add_dialog(TextPrompt("interpret_user_intention"))
        self.add_dialog(ChoicePrompt(ChoicePrompt.__name__))
        self.initial_dialog_id = WaterfallDialog.__name__
        self.add_dialog(TextPrompt(TextPrompt.__name__))

    async def options_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
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

        lista_estado_2 = "The items in the list are:\n" + self.current_order.show_items()

        print(lista_estado_2)

        await step_context.context.send_activity(
             MessageFactory.text(lista_estado_2)
        )

        message_text = (
            str(step_context.options)
            if step_context.options
            else "What can I help you with today?"
        )
        prompt_message = MessageFactory.text(
            message_text, message_text
        )

        return await step_context.prompt(
            TextPrompt.__name__, PromptOptions(prompt=prompt_message)
        )

    async def interpret_user_intention(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """
            New step that interprets the user intent, using a split and invoking add and remove
        """
        step_context.values["input"] = step_context.result
        query = step_context.result

        splitted = query.split()

        # having the splitted array:
        await step_context.context.send_activity(
            MessageFactory.text("Your action is: " + splitted[0])
        )

        await step_context.context.send_activity(
            MessageFactory.text("Your quantity is: " + splitted[1])
        )

        await step_context.context.send_activity(
            MessageFactory.text("Your Item is: " + splitted[2])
        )
        unit = Unit(1)
        item_x = None

        # I dont know if this is going to work
        itm = list(filter(lambda item: item.description == splitted[2], self.current_order.item_list))
        if splitted[0] == 'Add':
            self.current_order.add_item(float(splitted[1]), itm[0])
        elif splitted[0] == 'Remove':
            self.current_order.remove_item(float(splitted[1]), itm[0])

        lista_estado_3 = "The items in the list are:\n" + self.current_order.show_items()
        print(lista_estado_3)

        await step_context.context.send_activity(
             MessageFactory.text(lista_estado_3)
        )

        # if step_context.result.value == 'Portfolio':
        #     await step_context.context.send_activity(
        #         MessageFactory.text(f"Very well, this is your portfolio.")
        #     )
        #     # await step_context.context.send_activity(
        #     #     MessageFactory.text("We could and should use a Card here.")
        #     # )
        #
        #     # Verify that the operation object has ALL the info needed.
        #     card = self.create_table_style_card()
        #
        #     response = create_activity_reply(
        #         step_context.context.activity, "", "", [card]
        #     )
        #     await step_context.context.send_activity(response)
        #
        #     img_result = self.portfolio.show()
        #
        #     # Replace this text for a CARD
        #     await step_context.context.send_activity(
        #        MessageFactory.text(self.portfolio.show())
        #     )
        #
        #     # review if this can be deleted and dependant methods too
        #     # reply = Activity(type=ActivityTypes.message)
        #     # reply.text = "Portfolio image."
        #     # reply.attachments = [self.get_plot_img()]
        #     # await step_context.context.send_activity(reply)
        #
        #     # Portfolio distribution (cake)
        #     reply_cake = Activity(type=ActivityTypes.message)
        #     reply_cake.text = "Portfolio Distribution."
        #     reply_cake.attachments = [self.get_cake_img()]
        #     await step_context.context.send_activity(reply_cake)
        #
        #     # Here, the conversation can continue, or be terminated and reset
        #     return await step_context.end_dialog()
        #
        # elif step_context.result.value == 'Trade':
        #     await step_context.context.send_activity(
        #         MessageFactory.text(f"Ok, you want to trade.")
        #     )
        #     return await step_context.prompt(
        #         "text_prompt_input",
        #         PromptOptions(prompt=MessageFactory.text("What do you want to buy or sell?")),
        #     )
        #     # Here we wait for a TextPrompt input, that should contain the user intent,
        #     # like:
        #     # Buy 25 MSFT for $ 120
        #
        #     # here, we can also have a Choice Prompt based on our current holdings.
        #     # that way, the user intent, is getting narrowed in a interactive fashion.
        #
        # elif step_context.result.value == 'Help':
        #     await step_context.context.send_activity(
        #         MessageFactory.text(f"Some day, when the sun is bright in the sky and all the backlog tasks are completed, I will be able to give you help. Sorry.")
        #     )

        return await step_context.end_dialog()

    async def third_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """ TODO: Add description for OrderDialog.second_step """
        return_response = "Bye!"

        await step_context.context.send_activity(
            MessageFactory.text(return_response)
        )

        return await step_context.end_dialog()

