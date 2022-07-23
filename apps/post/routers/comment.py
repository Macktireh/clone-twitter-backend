from django.urls import path

from apps.post.views import CommentPostViewSet
from apps.post.routers.post import method_list_create, method_detail_update_delete


urlpatterns = [
    path('', CommentPostViewSet.as_view(method_list_create), name='list_or_create-comment'),
    path('<int:pk>/', CommentPostViewSet.as_view(method_detail_update_delete), name='detail_update_delete-comment'),
]