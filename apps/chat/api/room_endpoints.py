# List rooms


from typing import List
from django.shortcuts import get_object_or_404
from ninja import Router
from django.contrib.auth.models import User
from apps.chat.models import Message, Room
from ninja.errors import HttpError

from apps.chat.schemas import AddMembersSchema, MessageIn, MessageOut, RoomIn, RoomOut, RoomWithMembersIn


router = Router()



@router.get("/rooms", response=List[RoomOut])
def list_rooms(request):
    return list(Room.objects.values("id", "name"))

# Create room
@router.post("/rooms", response=RoomOut)
def create_room(request, payload: RoomIn):
    if Room.objects.filter(name=payload.name).exists():
        raise HttpError(400, "Room already exists")
    room = Room.objects.create(name=payload.name)
    return room

# Create room with members
@router.post("/rooms/with-members")
def create_room_with_members(request, payload: RoomWithMembersIn):
    if Room.objects.filter(name=payload.name).exists():
        raise HttpError(400, "Room already exists")
    room = Room.objects.create(name=payload.name)
    users = User.objects.filter(username__in=payload.members)
    room.members.set(users)
    return {
        "room": room.name,
        "members": [user.username for user in users]
    }

# ✅ Add members to existing room
@router.post("/rooms/{room_id}/add-members")
def add_members_to_room(request, room_id: int, payload: AddMembersSchema):
    try:
        room = Room.objects.get(id=room_id)
    except Room.DoesNotExist:
        raise HttpError(404, "Room not found")

    users_to_add = User.objects.filter(username__in=payload.members)
    if not users_to_add:
        raise HttpError(404, "No valid users found")

    room.members.add(*users_to_add)
    return {
        "room": room.name,
        "added_members": [user.username for user in users_to_add],
        "all_members": [user.username for user in room.members.all()]
    }


@router.get("/rooms/{room_id}/messages", response=List[MessageOut])
def get_room_messages(request, room_id: int):
    room = get_object_or_404(Room, id=room_id)
    messages = Message.objects.filter(room=room).order_by("timestamp")
    return [
        MessageOut(
            id=m.id,
            username=m.user.username,
            room=m.room.name,
            content=m.content,
            timestamp=m.timestamp,
        ) for m in messages
    ]
