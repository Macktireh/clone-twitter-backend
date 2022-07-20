from django.urls import path

from apps.post.views import LikePostViewSet
from apps.post.routers.post import method_list_create


urlpatterns = [
    path('', LikePostViewSet.as_view(method_list_create), name='list_or_create-likes'),
]