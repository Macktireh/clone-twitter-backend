from django.urls import include, path

from apps.profiles import views
from apps.utils import getList, getRetrieve, patchUpdate


urlpatterns = [
    path('me/', views.UserProfileViewSet.as_view(getList), name='getCurrentUser'),
    path('me/<str:public_id>/', views.UserProfileViewSet.as_view(patchUpdate), name='RetrieveUpdateCurrentUser'),
    path('', views.AllUserProfileViewSet.as_view(getList), name='getAllUser'),
]