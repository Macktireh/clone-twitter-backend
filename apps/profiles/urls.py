from django.urls import path

from apps.profiles import views


urlpatterns = [
    path('me/', views.GetUserProfileView.as_view(), name='me'),
    # path('<id>/update/', views.update_user_profile_view, name='profile_update'),
]