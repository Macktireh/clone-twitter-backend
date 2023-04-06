import os


from django.urls import path
from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter

from config.wsgi import *
from apps.ws.middleware import TokenAuthMiddlewareStack
from apps.ws.consumers import NotificationConsumer


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': 
        # TokenAuthMiddlewareStack(
            URLRouter(
                [
                    path('ws/notification/', NotificationConsumer.as_asgi())
                ]
            )
        # ),
})

app = application
