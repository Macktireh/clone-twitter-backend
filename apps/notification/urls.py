from django.urls import path

from apps.notification import views
from apps.utils import getList, getRetrieve, patchUpdate


urlpatterns = [
    path('', views.NotificationViewSet.as_view(getList), name='GetNotifications'),
    path('seen/', views.NotificationSeenReadViewSet.as_view(getList), name='SeenNotifications'),
    path('read/<str:publicId>/', views.NotificationSeenReadViewSet.as_view(getRetrieve), name='ReadNotification'),
]