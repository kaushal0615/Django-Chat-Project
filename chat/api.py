from ninja import NinjaAPI
from .models import Message, Room
from django.contrib.auth.models import User
from pydantic import BaseModel
from typing import List
from datetime import datetime

api = NinjaAPI()

class MessageSchema(BaseModel):
    id: int
    user: str
    room: str
    content: str
    timestamp: datetime


class MessageCreateSchema(BaseModel):
    username: str
    room: str
    content: str

# Get all messages

@api.get("/messages", response=List[MessageSchema])
def get_messages(request):
    return [
        MessageSchema(
            id=m.id,
            user=m.user.username,
            room=m.room.name,
            content=m.content,
            timestamp=m.timestamp
        ) for m in Message.objects.select_related("user", "room").all()
    ]


# Post new message

@api.post("/messages", response=MessageSchema)
def create_message(request, payload: MessageCreateSchema):
    user = User.objects.get(username=payload.username)
    room, _ = Room.objects.get_or_create(name=payload.room)

    message = Message.objects.create(
        user=user,
        room=room,
        content=payload.content
    )

    return MessageSchema(
        id=message.id,
        user=message.user.username,
        room=message.room.name,
        content=message.content,
        timestamp=message.timestamp
    )
