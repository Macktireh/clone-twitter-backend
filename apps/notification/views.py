from django.contrib.auth import get_user_model

from rest_framework import viewsets, status
from rest_framework.response import Response

from apps.notification.models import Notification
from apps.notification.serializers import NotificationSerializer
from apps.utils.response import response_messages


User = get_user_model()
res = response_messages('fr')


class NotificationViewSet(viewsets.ModelViewSet):
    
    queryset = Notification.objects.select_related('from_user').all()
    serializer_class = NotificationSerializer
    lookup_field = 'public_id'

    def list(self, request, *args, **kwargs):
        notifications = Notification.objects.my_notifications(request.user)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class NotificationSeenReadViewSet(viewsets.ModelViewSet):
    
    queryset = Notification.objects.select_related('from_user').all()
    serializer_class = NotificationSerializer
    lookup_field = 'public_id'

    def list(self, request, *args, **kwargs):
        notifications = Notification.objects.my_notifications(request.user)
        for notif in notifications:
            notif.seen = True
            notif.save()
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        publicId = kwargs.get('publicId', None)
        if not publicId:
            return Response({'errors': res["MISSING_PARAMETER"]}, status=status.HTTP_404_NOT_FOUND)
        try:
            notification = Notification.objects.get(public_id=publicId)
            if not notification.to_user == request.user:
                return Response({'errors': res["YOU_ARE_NOT_AUTHORIZED_FOR_THIS_ACTION"]}, status=status.HTTP_403_FORBIDDEN)
        except:
            return Response({'errors': res["YOU_ARE_NOT_AUTHORIZED_FOR_THIS_ACTION"]}, status=status.HTTP_403_FORBIDDEN)
        try:
            notification.read = True; notification.save()
            serializer = NotificationSerializer(notification)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'errors': res["SOMETHING_WENT_WRONG"]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)