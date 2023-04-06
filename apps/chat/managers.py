from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import Q


class MessageManager(models.Manager):
    
    def all_messages(self, current_user, other_user):
        from apps.chat.models import Message
        return Message.objects.filter(Q(reciever=current_user, sender=other_user) | Q(reciever=other_user, sender=current_user))
    
    def messages_received_not_seen(self, user):
        from apps.chat.models import Message
        return Message.objects.filter(reciever=user, seen=False)
    
    def messages_received_not_preview(self, user):
        from apps.chat.models import Message
        return Message.objects.filter(reciever=user, preview=False)