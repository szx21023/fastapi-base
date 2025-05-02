from abc import ABCMeta, abstractmethod
import asyncio

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import LineBotApiError
from linebot.models import TextMessage, TextSendMessage, MessageEvent

from ...exception.base_exception import LineBotException

class LineBot(metaclass=ABCMeta):
    def __init__(self, channel_access_token: str, channel_secret: str):
        self.channel_access_token = channel_access_token
        self.channel_secret = channel_secret
        self.line_bot_api = LineBotApi(self.channel_access_token)
        self.handler = WebhookHandler(self.channel_secret)

        self.register_handlers()

    async def reply_message(self, event, text: str):
        try:
            self.line_bot_api.reply_message(event.reply_token, TextMessage(text=text))

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

    @abstractmethod
    async def handle_message(self):
        """
        Each bot should define what handle_message it wants.
        """

    def register_handlers(self):
        @self.handler.add(MessageEvent, message=TextMessage)
        def handle_message(event: MessageEvent):
            message = f'line_event: {event}'
            self.logger.info(message)
            asyncio.create_task(self.handle_message(event))