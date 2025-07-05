from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
import json
from .models import Room

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        username = data.get("username")
        message = data.get("message")
        typing = data.get("typing")

        # Get user object (optional)
        user = await self.get_user(username)

        if typing:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "user_typing",
                    "username": user.username if user else "Anonymous"
                }
            )
        elif message:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "username": user.username if user else "Anonymous"
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "message",
            "username": event["username"],
            "message": event["message"]
        }))

    async def user_typing(self, event):
        await self.send(text_data=json.dumps({
            "type": "typing",
            "username": event["username"]
        }))

    @database_sync_to_async
    def get_user(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None

class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.other_user = self.scope["url_route"]["kwargs"]["username"]
        self.current_user = None  # will set after receiving first message
        self.room_group_name = None
        await self.accept()

    async def disconnect(self, close_code):
        if self.room_group_name:
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)

        # First message must include username
        if not self.current_user:
            self.current_user = data.get("username")
            if not self.current_user:
                await self.send(text_data=json.dumps({
                    "error": "Missing username"
                }))
                return

            # consistent ordering to avoid duplication
            user1, user2 = sorted([self.current_user, self.other_user])
            self.room_group_name = f"private_{user1}_{user2}"
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'private_message',
                'message': data.get('message'),
                'username': self.current_user
            }
        )

    async def private_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username']
        }))

class GroupChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"group_{self.room_name}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)  # Missing line
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
            await self.send(text_data=json.dumps({
                "type": "error",
                "message": "Room does not exist."
            }))
            return

        # Check membership before letting them chat or type
        if not user or not await self.is_member(room, user):
            await self.send(text_data=json.dumps({
                "type": "error",
                "message": "You are not a member of this room."
            }))
            return

        # Typing event
        if typing:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "user_typing",
                    "username": username
                }
            )
        elif message:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    "username": username
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "message",
            "username": event["username"],
            "message": event["message"]
        }))

    async def user_typing(self, event):
        await self.send(text_data=json.dumps({
            "type": "typing",
            "username": event["username"]
        }))

    @database_sync_to_async
    def get_user(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None

    @database_sync_to_async
    def get_room(self, room_name):
        try:
            return Room.objects.get(name=room_name)
        except Room.DoesNotExist:
            return None

    @database_sync_to_async
    def is_member(self, room, user):
        return room.members.filter(id=user.id).exists()
