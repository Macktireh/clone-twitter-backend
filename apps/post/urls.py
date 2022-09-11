from django.urls import include, path

from apps.post import views
from apps.utils import getList, postCreate, getRetrieve, putUpdate, patchUpdate, deleteDestroy


urlpatterns = [
    path('', views.PostViewSet.as_view({**getList, **postCreate}), name='ListCreatePost'),
    path('<str:public_id>/', views.PostViewSet.as_view({**getRetrieve, **putUpdate, **patchUpdate, **deleteDestroy}), name='RetrieveUpdateDeletePost'),
    path('likes/', views.LikePostViewSet.as_view({**getList, **postCreate}), name='GetCreateDeleteLikePost'),
]