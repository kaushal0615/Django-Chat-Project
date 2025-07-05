# chat/consumers/group_consumer.py
import json

from apps.chat.models import Room
from .base import BaseChatConsumer
from channels.db import database_sync_to_async


class GroupChatConsumer(BaseChatConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"group_{self.room_name}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        username = data.get("username")
        message = data.get("message")
        typing = data.get("typing")

        user = await self.get_user(username)
        room = await self.get_room(self.room_name)

        if not room:
            await self.send_json({"type": "error", "message": "Room does not exist."})
            return

        if not user or not await self.is_member(room, user):
            await self.send_json({"type": "error", "message": "You are not a member of this room."})
            return

        if typing:
            await self.channel_layer.group_send(self.room_group_name, {
                "type": "user_typing",
                "username": username
            })
        elif message:
            await self.channel_layer.group_send(self.room_group_name, {
                "type": "chat_message",
                "message": message,
                "username": username
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

    @database_sync_to_async
    def get_room(self, room_name):
        try:
            return Room.objects.get(name=room_name)
        except Room.DoesNotExist:
            return None

    @database_sync_to_async
    def is_member(self, room, user):
        return room.members.filter(id=user.id).exists()
