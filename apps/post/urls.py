from django.urls import path

from apps.post import views
from apps.utils import getList, postCreate, getRetrieve, putUpdate, patchUpdate, deleteDestroy


urlpatterns = [
    path('likes/', views.LikePostViewSet.as_view({**getList, **postCreate}), name='GetCreateDeleteLikePost'),
    path('likes/<str:userPublicId>/', views.ListPostsLikesViewSet.as_view({**getList}), name='ListPostsLikes'),
    path('', views.PostViewSet.as_view({**getList, **postCreate}), name='ListCreatePost'),
    path('<str:public_id>/', views.PostViewSet.as_view({**getRetrieve, **patchUpdate, **deleteDestroy}), name='RetrieveUpdateDeletePost'),
]