from django.urls import path

from apps.notification import views
from apps.utils import getList, getRetrieve, patchUpdate


urlpatterns = [
    path('', views.NotificationViewSet.as_view(getList), name='GetNotifications'),
]