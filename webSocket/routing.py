from django.urls import path

from webSocket.consumers import notification

websocket_urlpatterns = [
    path('ws/notification/', notification.NotificationConsumer.as_asgi())
]