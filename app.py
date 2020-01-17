import json
import os
import sys
import traceback
from datetime import datetime

import certifi
import slack
from aiohttp import web
from aiohttp.web import Request, Response, json_response
from botbuilder.core import (
    BotFrameworkAdapterSettings,
    TurnContext,
    BotFrameworkAdapter,
    MemoryStorage,
    ConversationState,
    UserState,
)
from botbuilder.core.integration import aiohttp_error_middleware
from botbuilder.schema import Activity, ActivityTypes

from bots import OrderBot
from config import DefaultConfig
from dialogs import OrderDialog

CONFIG = DefaultConfig()

# Create adapter.
# See https://aka.ms/about-bot-adapter to learn more about how bots work.
SETTINGS = BotFrameworkAdapterSettings(CONFIG.APP_ID, CONFIG.APP_PASSWORD)
ADAPTER = BotFrameworkAdapter(SETTINGS)


# Catch-all for errors.
async def on_error(context: TurnContext, error: Exception):
    # This check writes out errors to console log .vs. app insights.
    # NOTE: In production environment, you should consider logging this to Azure
    #       application insights.
    print(f"\n [on_turn_error] unhandled error: {error}", file=sys.stderr)
    traceback.print_exc()

    # Send a message to the user
    await context.send_activity("The bot encountered an error or bug.")
    await context.send_activity(
        "To continue to run this bot, please fix the bot source code."
    )
    # Send a trace activity if we're talking to the Bot Framework Emulator
    if context.activity.channel_id == "emulator":
        # Create a trace activity that contains the error object
        trace_activity = Activity(
            label="TurnError",
            name="on_turn_error Trace",
            timestamp=datetime.utcnow(),
            type=ActivityTypes.trace,
            value=f"{error}",
            value_type="https://www.botframework.com/schemas/error",
        )
        # Send a trace activity, which will be displayed in Bot Framework Emulator
        await context.send_activity(trace_activity)


ADAPTER.on_turn_error = on_error

# Create MemoryStorage, UserState and ConversationState
MEMORY = MemoryStorage()
CONVERSATION_STATE = ConversationState(MEMORY)
USER_STATE = UserState(MEMORY)

# create main dialog and bot
DIALOG = OrderDialog(USER_STATE)
BOT = OrderBot(CONVERSATION_STATE, USER_STATE, DIALOG)

@slack.RTMClient.run_on(event="message")
def message(**payload):
    """Display the onboarding welcome message after receiving a message
    that contains "start".
    """
    data = payload["data"]
    web_client = payload["web_client"]
    channel_id = data.get("channel")
    user_id = data.get("user")
    text = data.get("text")

    card_path = os.path.join(os.getcwd(), "resources/Card.json")
    with open(card_path, "rb") as in_file:
        card_data = json.load(in_file)
    print(card_data)
    web_client.chat_postMessage(channel=CONFIG.USER_ID, blocks=json.dumps(card_data))



APP = web.Application(middlewares=[aiohttp_error_middleware])
APP.router.add_post("/api/messages", message)


import ssl as ssl_lib

if __name__ == "__main__":
    try:
        ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
        slack_token = CONFIG.SLACK_BOT_TOKEN
        print(slack_token)
        rtm_client = slack.RTMClient(token=slack_token, ssl=ssl_context)
        rtm_client.start()
    except Exception as error:
        raise error
