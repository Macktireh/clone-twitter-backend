
from django.contrib import admin

from apps.chat.models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('created', 'sender', 'reciever', 'message', 'seen',)
    list_editable = ('seen',)
    list_filter = ('seen', 'created',)

