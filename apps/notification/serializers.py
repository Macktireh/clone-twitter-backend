from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from rest_framework import serializers

from apps.notification.models import Notification
from apps.profiles.serializers import UserSerializer
from apps.utils.response import response_messages


User = get_user_model()
res = response_messages('fr')


class NotificationSerializer(serializers.ModelSerializer):

    fromId = serializers.CharField(source='from_user.publi_id', read_only=True)
    toId = serializers.CharField(source='to_user.publi_id', read_only=True)

    class Meta:
        model = Notification
        fields = ['public_id', 'fromId', 'toId', 'seen', 'read', 'created', 'updated']
        read_only_fields = ['public_id', 'seen', 'read', 'created', 'updated']