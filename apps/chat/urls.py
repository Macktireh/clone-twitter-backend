from django.urls import path

from apps.chat.views import MessagesViewSet, MessagesNotificationViewSet
from apps.utils import getList, postCreate, deleteDestroy


urlpatterns = [
    path('<str:publicId>/', MessagesViewSet.as_view({**getList, **postCreate}), name='GetCreateDeleteMessages'),
    path('messages/notifications/', MessagesNotificationViewSet.as_view({**getList, **postCreate}), name='GetMessagesNotification'),
]