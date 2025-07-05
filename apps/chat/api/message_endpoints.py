from typing import List
from django.contrib.auth.models import User
from ninja import Router

from apps.chat.models import Message, Room
from apps.chat.schemas import MessageIn, MessageOut

from ninja.errors import HttpError

router = Router()


@router.get("/messages", response=List[MessageOut])
def get_messages(request):
    messages = Message.objects.all().order_by("timestamp")
    return [
        MessageOut(
            id=m.id,
            username=m.user.username,
            room=m.room.name,
            content=m.content,
            timestamp=m.timestamp,
        ) for m in messages
    ]

# Send a message
@router.post("/messages")
def create_message(request, payload: MessageIn):
    try:
        user = User.objects.get(username=payload.username)
        room = Room.objects.get(name=payload.room)
    except User.DoesNotExist:
        raise HttpError(404, "User not found")
    except Room.DoesNotExist:
        raise HttpError(404, "Room not found")

    msg = Message.objects.create(user=user, room=room, content=payload.content)
    return {"id": msg.id, "message": msg.content}