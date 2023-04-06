from django.contrib.auth import get_user_model

from rest_framework import viewsets, status
from rest_framework.response import Response

from apps.chat.models import Message
from apps.chat.serializers import MessageSerializer
from apps.utils.response import response_messages


User = get_user_model()
res = response_messages('fr')


class MessagesViewSet(viewsets.ModelViewSet):
    
    queryset = Message.objects.select_related('from_user').all()
    serializer_class = MessageSerializer
    lookup_field = 'public_id'
    
    def list(self, request, *args, **kwargs) -> Response:
        publicId = kwargs.get('publicId', None)
        if not publicId:
            return Response({'errors': res["MISSING_PARAMETER"]}, status=status.HTTP_404_NOT_FOUND)
        try:
            user = User.objects.get(public_id=publicId)
        except:
            return Response({'errors': res["SOMETHING_WENT_WRONG"]}, status=status.HTTP_403_FORBIDDEN)
        if not user:
            return Response({'errors': res["MISSING_PARAMETER"]}, status=status.HTTP_404_NOT_FOUND)
        try:
            messages = Message.objects.all_messages(current_user=request.user, other_user=user)
            for message in messages:
                message.seen = True
                message.save()
            serializer = MessageSerializer(messages, many=True)
        except:
            return Response({'errors': res["SOMETHING_WENT_WRONG"]}, status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MessagesNotificationViewSet(viewsets.ModelViewSet):
    
    queryset = Message.objects.select_related('from_user').all()
    serializer_class = MessageSerializer
    
    def list(self, request, *args, **kwargs):
        messages = Message.objects.messages_received_not_preview(request.user)
        return Response({"numberMessagesNotif": messages.count()}, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        messages = Message.objects.messages_received_not_preview(request.user)
        for message in messages:
                message.preview = True
                message.save()
        return Response({"numberMessagesNotif": 0}, status=status.HTTP_200_OK)