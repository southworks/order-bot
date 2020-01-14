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

import data_models.Constants as Constants
from data_models.Constants import Constants, ConstantUnits
from helpers import DialogHelper
from data_models import Unit, Item, Order, OrderStatus, Constants

from helpers import activity_helper

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
        step_context.values['input'] = step_context.result
        user_input = step_context.values['input'].lower()

        splitted_input = user_input.split()

        is_quantity = False
        has_unit = False

        for input in splitted_input:
            if input in ConstantUnits.units:
                has_unit = True
                unit = input

        results = parse_all(user_input, DEFAULT_CULTURE)

        match = ([sub_list for sub_list in results if sub_list][0]) if results else []

        for item in match:
            type_name = item.type_name
            if type_name == Constants.Constants.number_type_name:
                if '.' in item.resolution.get('value'):
                    has_unit = True
                    quantity = 0
                    weight = float(item.resolution.get('value'))
                else:
                    is_quantity = True
                    quantity = int(item.resolution.get('value'))
                    weight = 0
                    unit = 'unit'
            elif type_name == Constants.Constants.dimension_type_name:
                has_unit = True
                weight = item.resolution.get('value')
                quantity = 0
                unit = item.resolution.get('unit')

        action = DialogHelper.recognize_intention(user_input)

        if has_unit:
            if 'of' in user_input:
                user_input = user_input.replace('of', '')
            item_description = user_input[match[0].start + 7:].strip()
        else:
            user_input.strip()
            item_description = user_input[match[0].start + 2:].strip()

        item = next(
            (
                x
                for x in self.current_order.item_list
                if x.description.lower() == item_description.lower()
            ),
            None,
        )

        if not item and action.description != "confirmed":
            item = Item(
                product_id=self.current_order.item_list[-1].product_id + 1,
                description=item_description,
                item_id=self.current_order.item_list[-1].item_id + 1,
                quantity=quantity,
                weight=weight,
                unit=unit
            )

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

    async def show_action_taken(self, step_context, quantity=0, weight=0, item_description='', unit='', action=None):
        if quantity:
            await step_context.context.send_activity(
                MessageFactory.text(
                    f"{quantity} {item_description.capitalize()} was {action.description}!"
                )
            )
        elif weight:
            await step_context.context.send_activity(
                MessageFactory.text(
                    f"{weight} {unit} of {item_description.capitalize()} was {action.description}!"
                )
            )


def parse_all(user_input: str, culture: str) -> List[List[ModelResult]]:
    return [
        # Number recognizer - This function will find any number from the input
        # E.g "I have two apples" will return "2".
        recognizers_suite.recognize_number(user_input, culture),

        # Ordinal number recognizer - This function will find any ordinal number
        # E.g "eleventh" will return "11".
        recognizers_suite.recognize_ordinal(user_input, culture),

        # Percentage recognizer - This function will find any number presented as percentage
        # E.g "one hundred percents" will return "100%"
        recognizers_suite.recognize_percentage(user_input, culture),

        # Age recognizer - This function will find any age number presented
        # E.g "After ninety five years of age, perspectives change" will return
        # "95 Year"
        recognizers_suite.recognize_age(user_input, culture),

        # Currency recognizer - This function will find any currency presented
        # E.g "Interest expense in the 1988 third quarter was $ 75.3 million"
        # will return "75300000 Dollar"
        recognizers_suite.recognize_currency(user_input, culture),

        # Dimension recognizer - This function will find any dimension presented E.g "The six-mile trip to my airport
        # hotel that had taken 20 minutes earlier in the day took more than
        # three hours." will return "6 Mile"
        recognizers_suite.recognize_dimension(user_input, culture),

        # Temperature recognizer - This function will find any temperature presented
        # E.g "Set the temperature to 30 degrees celsius" will return "30 C"
        recognizers_suite.recognize_temperature(user_input, culture),

        # DateTime recognizer - This function will find any Date even if its write in colloquial language -
        # E.g "I'll go back 8pm today" will return "2017-10-04 20:00:00"
        recognizers_suite.recognize_datetime(user_input, culture),

        # PhoneNumber recognizer will find any phone number presented
        # E.g "My phone number is ( 19 ) 38294427."
        recognizers_suite.recognize_phone_number(user_input, culture),

        # Email recognizer will find any phone number presented
        # E.g "Please write to me at Dave@abc.com for more information on task
        # #A1"
        recognizers_suite.recognize_email(user_input, culture),

    ]