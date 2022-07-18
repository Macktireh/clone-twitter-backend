from django.urls import path

from apps.post.views import PostViewSet, CommentPostViewSet


method_list_create = {
    'get': 'list',
    'post': 'create'
}

method_detail_update_delete = {
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
}

urlpatterns = [
    path('', PostViewSet.as_view(method_list_create), name='list_or_create-post'),
    path('<int:pk>/', PostViewSet.as_view(method_detail_update_delete), name='detail_update_delete-post'),
    path('comment/', CommentPostViewSet.as_view(method_list_create), name='list_or_create-comment'),
    path('comment/<int:pk>/', CommentPostViewSet.as_view(method_detail_update_delete), name='detail_update_delete-comment'),
]