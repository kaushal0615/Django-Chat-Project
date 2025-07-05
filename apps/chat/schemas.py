from datetime import datetime
from typing import List
from ninja import Schema


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