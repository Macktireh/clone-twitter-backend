from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from apps.account import views


urlpatterns = [
    path('signup/', views.UserSignupView.as_view({'post': 'create'}), name='signup'),
    path('login/', views.UserLoginView.as_view({'post': 'create'}), name='login'),
    path('activate/', views.UserActivationView.as_view({'post': 'create'}), name='activate'),
    path('change-password/', views.UserChangePasswordView.as_view({'post': 'create'}), name='change_password'),
    path('reset-password-send-email/', views.SendEmailResetPasswordView.as_view({'post': 'create'}), name='reset_password_send_email'),
    path('reset-password/<uidb64>/<token>/', views.UserResetPasswordView.as_view({'post': 'create'}), name='reset_password'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]