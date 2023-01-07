from django.urls import path

from apps.bookmark import views
from apps.utils import getList, postCreate


urlpatterns = [
    path('', views.BookmarkViewSet.as_view({**getList, **postCreate}), name='GetCreateBookmark'),
]