# chat/consumers/private_consumer.py
import json
from .base import BaseChatConsumer

class PrivateChatConsumer(BaseChatConsumer):
    async def connect(self):
        self.other_user = self.scope["url_route"]["kwargs"]["username"]
        self.current_user = None
        self.room_group_name = None
        await self.accept()

    async def disconnect(self, close_code):
        if self.room_group_name:
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)

        if not self.current_user:
            self.current_user = data.get("username")
            if not self.current_user:
                await self.send_json({"error": "Missing username"})
                return

            user1, user2 = sorted([self.current_user, self.other_user])
            self.room_group_name = f"private_{user1}_{user2}"
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.channel_layer.group_send(self.room_group_name, {
            "type": "private_message",
            "message": data.get("message"),
            "username": self.current_user
        })

    async def private_message(self, event):
        await self.send_json({
            "type": "message",
            "username": event["username"],
            "message": event["message"]
        })
