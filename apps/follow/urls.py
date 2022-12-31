from django.urls import include, path

from apps.follow import views
from apps.utils import getList, postCreate


urlpatterns = [
    path('following/<str:userPublicId>/', views.FollowingViewSet.as_view({**getList, **postCreate}), name='following'),
    path('followers/<str:userPublicId>/', views.FollowersViewSet.as_view(getList), name='followers'),
    path('people-connect/', views.PeopleConnectViewSet.as_view(getList), name='people-connect'),
]