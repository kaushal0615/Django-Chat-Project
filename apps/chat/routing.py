from django.urls import path

from apps.chat.consumers.group_consumer import GroupChatConsumer
from apps.chat.consumers.private_consumer import PrivateChatConsumer
from apps.chat.consumers.public_consumer import ChatConsumer

websocket_urlpatterns = [
    path("ws/room/<str:room_name>/", ChatConsumer.as_asgi(), name="chat-room"),
    path("ws/private/<str:username>/", PrivateChatConsumer.as_asgi(), name="private-chat"),
    path("ws/group/<str:room_name>/", GroupChatConsumer.as_asgi(), name="group-chat"),
]


