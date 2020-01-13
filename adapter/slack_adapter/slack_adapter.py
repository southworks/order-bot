import slack
from botbuilder.schema import Activity

from slack_adapter import NewSlackMessage


class SlackAdapter:
    @property
    def __options(self):
        return self._options

    @property
    def __slack(self):
        return self._slack

    @property
    def __identity(self):
        return self._identity

    @property
    def name(self):
        return 'Slack Adapter'

    @property
    def middlewares(self):
        return self._middlewares

    def __init__(self, options):
        self._slack = slack.web

    @staticmethod
    def activity_to_slack(activity:Activity):
        channel_id = activity.conversation.id
        thread_time_stamp = activity.conversation.thread_time_stamp

        message = NewSlackMessage(time_stamp=activity.timestamp, text=activity.text, attachments=activity.attachments,
                                  channel=channel_id, thread_time_stamp=thread_time_stamp)

        if message.ephemeral:
            message.user = activity.recipient.id

        if not message.icon_url or message.icons or not message.username:
            message.as_user = False

        return message
