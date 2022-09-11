from django.urls import include, path

from apps.profiles import views
from apps.utils import getList, getRetrieve, patchUpdate


# router = routers.DefaultRouter()
# router.register('', views.UserProfileViewSet, basename='me')

# urlpatterns = [
#     path('', include(router.urls))
# ]


patchUpdate

urlpatterns = [
    path('me/', views.UserProfileViewSet.as_view(getList), name='getCurrentUser'),
    path('me/<str:public_id>/', views.UserProfileViewSet.as_view({**getRetrieve, **patchUpdate}), name='RetrieveUpdateCurrentUser'),
    path('all/', views.AllUserProfileViewSet.as_view(getList), name='getAllUser'),
]