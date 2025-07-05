from django.urls import re_path
from chat.consumer import GroupChatConsumer, ChatConsumer, PrivateChatConsumer

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),
    re_path(r"ws/private/(?P<username>\w+)/$", PrivateChatConsumer.as_asgi()),
    re_path(r"ws/chat/group/(?P<room_name>\w+)/$", GroupChatConsumer.as_asgi()),  
]

