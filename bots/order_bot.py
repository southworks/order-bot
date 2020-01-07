# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import (
    ActivityHandler,
    TurnContext,
    UserState,
    CardFactory,
    MessageFactory,
)
from botbuilder.schema import (
    ChannelAccount,
    HeroCard,
    CardImage,
    CardAction,
    ActionTypes,
)

from botbuilder.core import ActivityHandler, ConversationState, TurnContext, UserState, MessageFactory
from botbuilder.dialogs import Dialog

from helpers.dialog_helper import DialogHelper

from data_models.unit import Unit
from data_models.order import Order, OrderStatus
from data_models.item import Item


class OrderBot(ActivityHandler):
    """ TODO: Add description for OrderBot class """

    def __init__(
        self,
        conversation_state: ConversationState,
        user_state: UserState,
        dialog: Dialog,
    ):
        if conversation_state is None:
            raise TypeError(
                "[DialogBot]: Missing parameter. conversation_state is required but None was given"
            )
        if user_state is None:
            raise TypeError(
                "[DialogBot]: Missing parameter. user_state is required but None was given"
            )
        if dialog is None:
            raise Exception("[DialogBot]: Missing parameter. dialog is required")

        self.conversation_state = conversation_state
        self.user_state = user_state
        self.dialog = dialog
        self.user_state_accessor = self.user_state.create_property("WelcomeUserState")
        self.WELCOME_MESSAGE = """Hello user!"""

    async def on_turn(self, turn_context: TurnContext):
        await super().on_turn(turn_context)

        # Save any state changes that might have ocurred during the turn.
        await self.conversation_state.save_changes(turn_context)
        await self.user_state.save_changes(turn_context)

    async def on_members_added_activity(
        self, members_added: ChannelAccount, turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                reply = MessageFactory.text(
                    "Hello User! "
                    + "Please type anything to get started."
                )
                # TODO: Call to order object's items
                msg = "The list is:"
                await turn_context.send_activity(reply, msg)

    async def on_message_activity(self, turn_context: TurnContext):
        """
        Respond to messages sent from the user.
        """
        await DialogHelper.run_dialog(
            self.dialog,
            turn_context,
            self.conversation_state.create_property("DialogState"),
        )
