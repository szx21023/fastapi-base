from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import LineBotApiError
from linebot.models import TextMessage, TextSendMessage

from ...exception.base_exception import LineBotException

class LineBot:
    def __init__(self, channel_access_token: str, channel_secret: str):
        self.channel_access_token = channel_access_token
        self.channel_secret = channel_secret
        self.line_bot_api = LineBotApi(self.channel_access_token)
        self.handler = WebhookHandler(self.channel_secret)

    async def reply_message(self, event, message):
        try:
            self.line_bot_api.reply_message(event.reply_token, TextMessage(text=message))

        except LineBotApiError as err:
            exception = LineBotException(str(err))
            raise exception

    async def push_message(self, line_uid: str, text: str):
        try:
            self.line_bot_api.push_message(line_uid, TextSendMessage(text=text))

        except LineBotApiError as err:
            message = f"Send line message fail, line_uid: {line_uid}, text: {text}, err: {str(err)}"
            exception = LineBotException(message)
            raise exception