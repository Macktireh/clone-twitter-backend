from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import Q


class MessageManager(models.Manager):
    
    def all_messages(self, current_user, other_user):
        """
        Args:
            current_user : utilisateur actuelle ou connecté
            other_user : utilisateur qui chate avec l'utilisateur connecté
        Returns:
            cette méthode renvoie tout les messages entre ces deux utilisateurs
        """
        from apps.chat.models import Message
        return Message.objects.filter(Q(reciever=current_user, sender=other_user) | Q(reciever=other_user, sender=current_user))
