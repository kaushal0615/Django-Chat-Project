# chat/consumers/public_consumer.py
import json
from .base import BaseChatConsumer

class ChatConsumer(BaseChatConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        user = await self.get_user(data.get("username"))

        if data.get("typing"):
            await self.channel_layer.group_send(self.room_group_name, {
                "type": "user_typing",
                "username": user.username if user else "Anonymous"
            })
        elif data.get("message"):
            await self.channel_layer.group_send(self.room_group_name, {
                "type": "chat_message",
                "message": data["message"],
                "username": user.username if user else "Anonymous"
            })

    async def chat_message(self, event):
        await self.send_json({
            "type": "message",
            "username": event["username"],
            "message": event["message"]
        })

    async def user_typing(self, event):
        await self.send_json({
            "type": "typing",
            "username": event["username"]
        })
