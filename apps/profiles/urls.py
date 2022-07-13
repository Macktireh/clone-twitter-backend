from django.urls import path

from apps.profiles import views

from rest_framework import routers

router = routers.DefaultRouter()
router.register('me', views.UserProfileViewSet, basename='me')


# urlpatterns = [
#     path('me/', views.GetUserProfileView.as_view(), name='me'),
#     path('f/', views.my_profile_view, name='me'),
#     path('f/<int:id>/', views.my_profile_update_view, name='me-update'),
# ]