from django.urls import include, path

from apps.comment import views
from apps.utils import getList, postCreate, getRetrieve, putUpdate, patchUpdate, deleteDestroy


urlpatterns = [
    path('likes/', views.LikeCommentViewSet.as_view({**getList, **postCreate}), name='GetCreateDeleteLikeComment'),
    path('', views.CommentPostViewSet.as_view({**getList, **postCreate}), name='ListCreateComment'),
    path('<str:public_id>/', views.CommentPostViewSet.as_view({**getRetrieve, **patchUpdate, **deleteDestroy}), name='RetrieveUpdateDeleteComment'),
]