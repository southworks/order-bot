import slack
from botbuilder.schema import Activity

from slack_adapter import NewSlackMessage

Object = lambda **kwargs: type("Object", (), kwargs)

def activity_to_slack(activity: Activity):
    if not activity:
        raise Exception

    message = NewSlackMessage()
    if not activity.timestamp:
        attachments = []

        for att in activity.attachments:
            if att.name == 'blocks':
                message.blocks = [att.content]
            else:
                new_attachment = Object(author_name= att.name, thumb_url=att.thumbnail_url)