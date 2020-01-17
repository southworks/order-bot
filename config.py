#!/usr/bin/env python3


import os


""" Bot Configuration """


class DefaultConfig:
    """ Bot Configuration """

    PORT = 3978
    APP_ID = os.environ.get("MicrosoftAppId", "")
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
    USER_ID = os.getenv("USER_ID")
