# chat/consumers/base.py
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
import json

class BaseChatConsumer(AsyncWebsocketConsumer):
    async def receive_json(self, content, **kwargs):
        # If you prefer receive_json, override here
        pass

    async def send_json(self, content):
        await self.send(text_data=json.dumps(content))

    @database_sync_to_async
    def get_user(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None
