from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from rest_framework import serializers

from apps.notification.models import Notification
from apps.utils.response import response_messages


User = get_user_model()
res = response_messages('fr')


class NotificationSerializer(serializers.ModelSerializer):

    publicId = serializers.CharField(source='public_id', read_only=True)
    typeNotif = serializers.CharField(source='type_notif', read_only=True)
    fromId = serializers.CharField(source='from_user.public_id', read_only=True)
    toId = serializers.CharField(source='to_user.public_id', read_only=True)
    postPublicId = serializers.CharField(source='post.public_id', read_only=True)
    post = serializers.CharField(source='post.body', read_only=True)
    comment = serializers.CharField(source='comment_post.message', read_only=True)

    class Meta:
        model = Notification
        fields = ['publicId', 'fromId', 'toId', 'typeNotif', 'postPublicId', 'post', 'comment', 'seen', 'read', 'created', 'updated']
        read_only_fields = ['seen', 'read', 'created', 'updated']