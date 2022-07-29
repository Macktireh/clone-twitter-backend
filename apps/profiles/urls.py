from django.urls import include, path

from rest_framework import routers

from apps.profiles import views


router = routers.DefaultRouter()
router.register('', views.UserProfileViewSet, basename='me')

urlpatterns = [
    path('', include(router.urls))
]