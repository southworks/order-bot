class NewSlackMessage:

    @property
    def ephemeral(self):
        return self._ephemeral

    @property
    def as_user(self):
        return self._as_user

    @as_user.setter
    def as_user(self, as_user):
        self._as_user = as_user

    @property
    def icon_url(self):
        return self._icon_url

    @property
    def icon_emoji(self):
        return self._icon_emoji

    @property
    def thread_time_stamp(self):
        return self._thread_time_stamp

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user):
        self._user = user

    @property
    def channel(self):
        return self._channel

    @property
    def text(self):
        return self._text

    @property
    def team(self):
        return self._team

    @property
    def time_stamp(self):
        return self._time_stamp

    @property
    def username(self):
        return self._username

    @property
    def bot_id(self):
        return self._bot_id

    @property
    def icons(self):
        return self._icons

    @property
    def blocks(self):
        return self._blocks

    @blocks.setter
    def blocks(self, blocks):
        self._blocks = blocks

    @property
    def attachments(self):
        return self._attachments

    def __init__(self, ephemeral=None, as_user=None, icon_url=None, time_stamp=None, text=None, attachments=None,
                 channel=None, thread_time_stamp=None, icons=None, icon_emoji=None, username=None, user=None, team=None,
                 bot_id=None):
        self._ephemeral = ephemeral
        self._as_user = as_user
        self._icon_url = icon_url
        self._time_stamp = time_stamp
        self._text = text
        self._channel = channel
        self._thread_time_stamp = thread_time_stamp
        self._attachments = attachments
        self._icons = icons
        self._icon_emoji = icon_emoji
        self._user = user
        self._team = team
        self._username =username
        self._bot_id = bot_id