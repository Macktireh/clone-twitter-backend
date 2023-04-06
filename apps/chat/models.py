
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from apps.chat.managers import MessageManager


User = get_user_model()


class Message(models.Model):
    
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    reciever = models.ForeignKey(User, related_name='reciever', on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    seen = models.BooleanField(default=False)
    preview = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created',]
    
    objects = MessageManager()
    
    def __str__(self) -> str:
        return f"CHAT sender: {self.sender.first_name} | reciever: {self.reciever.first_name}"
    
    def get_messages(self) -> str:
        return f"{self.message}"
