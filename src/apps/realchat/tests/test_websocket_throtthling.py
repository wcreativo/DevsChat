from django.test import TestCase
from channels.testing import WebsocketCommunicator
from apps.realchat.consumers import ChatConsumer
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from apps.realchat.middleware.websocket_throttling import WebSocketThrottlingMiddleware
from apps.realchat.routing import websocket_urlpatterns

class WebSocketThrottlingMiddlewareTest(TestCase):
    async def test_chat_consumer(self):
        django_asgi_app = get_asgi_application()

        application = ProtocolTypeRouter(
            {
                "http": django_asgi_app,
                "websocket": AllowedHostsOriginValidator(
                    AuthMiddlewareStack(
                        WebSocketThrottlingMiddleware(
                            URLRouter(websocket_urlpatterns), rate_limit=1
                        )
                    )
                ),
            }
        )
        communicator = WebsocketCommunicator(application, "ws/chat/copernico/")
        connected, subprotocol = await communicator.connect()
        assert connected
