
from django.contrib import admin

from apps.chat.models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('created', '_sender', '_reciever', 'message', 'seen', 'preview',)
    list_editable = ('seen', 'preview',)
    list_filter = ('seen', 'created',)
    
    def _sender(self, instance):
        return f"{instance.sender.get_full_name()}"
    
    def _reciever(self, instance):
        return f"{instance.reciever.get_full_name()}"
