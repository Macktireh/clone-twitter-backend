import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from apps.notification.models import Notification


class NotificationConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.notif_group = "notif_group"

    def connect(self):
        
        self.accept()

        async_to_sync(self.channel_layer.group_add)(
            self.notif_group,
            self.channel_name,
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.notif_group,
            self.channel_name,
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # send chat message event to the room
        async_to_sync(self.channel_layer.group_send)(
            self.notif_group,
            {
                'type': 'notif_message',
                'message': message,
            }
        )

    def notif_message(self, event):
        self.send(text_data=json.dumps(event))