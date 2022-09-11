from django.urls import path

from apps.post.views import PostViewSet


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
    path('<str:public_id>/', PostViewSet.as_view(method_detail_update_delete), name='detail_update_delete-post'),
]