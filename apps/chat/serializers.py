from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from rest_framework import serializers

from apps.chat.models import Message
from apps.profiles.serializers import UserSerializer
from apps.utils.response import response_messages


User = get_user_model()
res = response_messages('fr')


class MessageSerializer(serializers.ModelSerializer):

    sender = UserSerializer(read_only=True)
    reciever = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['sender', 'reciever', 'message', 'seen', 'preview', 'created', 'updated']
        read_only_fields = ['seen', 'preview', 'created', 'updated']