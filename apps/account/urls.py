from django.urls import path

from apps.account import views


urlpatterns = [
    path('signup/', views.UserSignupView.as_view(), name='signup'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('activate-user/<uidb64>/<token>/', views.user_activate_account_view, name='activate'),
    path('change-password/', views.UserChangePasswordView.as_view(), name='change_password'),
    path('reset-password-send-email/', views.SendEmailResetPasswordView.as_view(), name='reset_password_send_email'),
    path('reset-password/<uidb64>/<token>/', views.UserResetPasswordView.as_view(), name='reset_password'),
]