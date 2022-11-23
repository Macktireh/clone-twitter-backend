from rest_framework import viewsets

from apps.notification.models import Notification
from apps.notification.serializers import NotificationSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    
    queryset = Notification.objects.select_related('from_user').all()
    serializer_class = NotificationSerializer
    lookup_field = 'public_id'
