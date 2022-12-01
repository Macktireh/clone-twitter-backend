from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model

from apps.utils.functions import list_to_queryset


User = get_user_model()


class NotificationManager(models.Manager):

    def my_notifications(self, me):
        from apps.notification.models import Notification
        return Notification.objects.select_related('to_user').filter(to_user=me)