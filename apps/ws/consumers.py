import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from apps.notification.models import Notification


class NotificationConsumerProtected(WebsocketConsumer):
    
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.notif_group = "notif_group"
        self.user = None
        self.user_inbox = None
    
    def connect(self):
        self.user = self.scope['user']
        if self.user.is_anonymous:
            self.close()
        elif self.user.is_authenticated:
            self.user_inbox = f'inbox_{self.user.public_id}'
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
        if not self.user.is_authenticated:  # new
            return
        
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        async_to_sync(self.channel_layer.group_send)(
            self.notif_group,
            {
                'type': 'message_notification' if message == 'Send_Message' else 'other_notifications',
                'message': message,
            }
        )
    
    def other_notifications(self, event):
        self.send(text_data=json.dumps(event))
    
    def message_notification(self, event):
        self.send(text_data=json.dumps(event))


class NotificationConsumer(WebsocketConsumer):
    
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.notif_group = "notif_group"
        self.user = None
        self.user_inbox = None
    
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
        # if not self.user.is_authenticated:  # new
        #     return
        
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        async_to_sync(self.channel_layer.group_send)(
            self.notif_group,
            {
                'type': 'message_notification' if message == 'Send_Message' else 'other_notifications',
                'message': message,
            }
        )
    
    def other_notifications(self, event):
        self.send(text_data=json.dumps(event))
    
    def message_notification(self, event):
        self.send(text_data=json.dumps(event))
