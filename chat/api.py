from ninja import NinjaAPI
from .models import Message
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
