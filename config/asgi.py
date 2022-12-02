import os


from django.urls import path
from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter

from config.wsgi import *
from apps.notification import consumers as notification


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': URLRouter(
        [
            path('ws/notification/', notification.NotificationConsumer.as_asgi())
        ]
    ),
})