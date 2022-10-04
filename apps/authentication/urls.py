from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from apps.authentication import views


urlpatterns = [
    path('signup/', views.SignupView.as_view({'post': 'create'}), name='signup'),
    path('account/activation/', views.ActivationView.as_view({'post': 'create'}), name='activate'),
    path('login/', views.LoginView.as_view({'post': 'create'}), name='login'),
    path('change-password/', views.UserChangePasswordView.as_view({'post': 'create'}), name='change_password'),
    path('request/reset-password/', views.RequestResetPasswordView.as_view({'post': 'create'}), name='reset_password_send_email'),
    path('reset-password/<uidb64>/<token>/', views.UserResetPasswordView.as_view({'post': 'create'}), name='reset_password'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='verify_jwt'),
    path('logout/', views.LogoutView.as_view({'post': 'create'}), name='logout'),
]