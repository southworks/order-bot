# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

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

from typing import List


class OrderDialog(ComponentDialog):
    """ TODO: Add description for OrderDialog class. """
    def __init__(self, user_state: UserState):
        super(OrderDialog, self).__init__(OrderDialog.__name__)
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
        """ TODO: Add description for OrderDialog.options_step """
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

