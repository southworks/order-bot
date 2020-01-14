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

from helpers import DialogHelper, activity_helper
from data_models import Order, OrderStatus, Constants
import recognizers_suite
from recognizers_suite import Culture, ModelResult

DEFAULT_CULTURE = Culture.English


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
            self.current_order = DialogHelper.init_dialog()

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
        unit = ''

        step_context.values['input'] = step_context.result
        user_input = step_context.values['input'].lower()

        results = [sub_list for sub_list in parse_all(user_input, DEFAULT_CULTURE) if sub_list]
        match = [item for sublist in results for item in sublist].pop()

        has_unit, weight, is_quantity, quantity, unit = DialogHelper.resolve_quantity_and_weigh(match)
        action = DialogHelper.recognize_intention(user_input)
        item_description = DialogHelper.normalize_description(has_unit, is_quantity, user_input, match)

        item = next(
            (
                x
                for x in self.current_order.item_list
                if x.description.lower() == item_description.lower()
            ),
            None,
        )

        action.create_item(self.current_order, quantity, weight, item_description, unit)
        action.execute(quantity, weight, self.current_order, item)

        if self.current_order.status == OrderStatus.Confirmed:
            if (
                type(step_context.result) is bool and not step_context.result
            ) or (
                type(step_context.result) is str
                and "confirm" not in step_context.result.lower()
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

        await self.show_action_taken(step_context, quantity, weight, item_description, unit, action)

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

    async def show_action_taken(self, step_context, quantity=None, weight=None, item_description='', unit='', action=None):
        if quantity:
            await step_context.context.send_activity(
                MessageFactory.text(
                    f"{quantity} {item_description} was {action.description}!"
                )
            )
        elif weight:
            await step_context.context.send_activity(
                MessageFactory.text(
                    f"{weight} {unit} of {item_description} was {action.description}!"
                )
            )


def parse_all(user_input: str, culture: str) -> List[List[ModelResult]]:
    return [
        # Number recognizer - This function will find any number from the input
        # E.g "I have two apples" will return "2".
        recognizers_suite.recognize_number(user_input, culture),

        # Dimension recognizer - This function will find any dimension presented E.g "The six-mile trip to my airport
        # hotel that had taken 20 minutes earlier in the day took more than
        # three hours." will return "6 Mile"
        recognizers_suite.recognize_dimension(user_input, culture),

    ]