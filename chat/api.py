# chat/api.py
from ninja import NinjaAPI, Schema, Router
from typing import List
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from ninja.errors import HttpError
from .models import Room, Message
from django.shortcuts import get_object_or_404
from datetime import datetime

# Initialize main API instance
api = NinjaAPI()

# Define a router to organize endpoints
router = Router()

# Schemas
class RegisterSchema(Schema):
    username: str
    password: str

class LoginSchema(Schema):
    username: str
    password: str

class MessageIn(Schema):
    username: str
    room: str
    content: str

class MessageOut(Schema):
    id: int
    username: str
    room: str
    content: str
    timestamp: datetime

class RoomIn(Schema):
    name: str

class RoomWithMembersIn(Schema):
    name: str
    members: List[str]

class AddMembersSchema(Schema):
    members: List[str]

class RoomOut(Schema):
    id: int
    name: str

class UserOut(Schema):
    id: int
    username: str

# Register endpoint
@router.post("/register")
def register_user(request, payload: RegisterSchema):
    if User.objects.filter(username=payload.username).exists():
        raise HttpError(400, "Username already taken")
    user = User.objects.create(
        username=payload.username,
        password=make_password(payload.password)
    )
    return {"id": user.id, "username": user.username}

# Login endpoint
@router.post("/login")
def login_user(request, payload: LoginSchema):
    user = authenticate(username=payload.username, password=payload.password)
    if user is None:
        raise HttpError(401, "Invalid credentials")
    return {"message": "Login successful", "user_id": user.id}

# List users
@router.get("/users", response=List[UserOut])
def list_users(request):
    return list(User.objects.values("id", "username"))

# List rooms
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

# Get all messages
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

# Get messages for a specific room
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

# Attach router to main API
api.add_router("", router)
