"""
ASGI config for chatninja project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""


import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatninja.settings')
django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing

application = ProtocolTypeRouter({
    # Handles traditional Django views, admin, API
    "http": get_asgi_application(),

    # Handles WebSocket connections for chat
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
