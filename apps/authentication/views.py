from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import gettext as _

from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated

from apps.utils.renderers import UserRenderer
from apps.authentication.tokens import get_tokens_for_user, generate_token
from apps.utils.email import send_email
from apps.authentication import serializers


User = get_user_model()


class UserSignupView(viewsets.ModelViewSet):

    renderer_classes = [UserRenderer]
    serializer_class = serializers.UserSignupSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = serializers.UserSignupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = generate_token.make_token(user)
            send_email(
                subject=f"Activation du compte sur {settings.DOMAIN_FRONTEND}", 
                template_name="authentication/mail/activate.html", 
                user=user, 
                token=token, 
                domain=settings.DOMAIN_FRONTEND
            )
            return Response(
                {'msg': _("Registration Successful")},
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UserActivationView(viewsets.ModelViewSet):

    renderer_classes = [UserRenderer]
    serializer_class = serializers.UserActivationSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = serializers.UserActivationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(
                {'msg': _("Your account has been successfully created and activated!")},
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UserLoginView(viewsets.ModelViewSet):

    renderer_classes = [UserRenderer]
    serializer_class = serializers.UserLoginSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = serializers.UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                _user = User.objects.get(email=user.email)
                if _user.is_verified_email:
                    token = get_tokens_for_user(user)
                    return Response(
                        {'msg': _("Login Success"), "token": token},
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {'errors': _("Veuillez confirmer votre adresse e-mail !")},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {'errors': _("L'email ou le mot de passe n'est pas valide !")},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UserChangePasswordView(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]
    renderer_classes = [UserRenderer]
    serializer_class = serializers.UserChangePasswordSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = serializers.UserChangePasswordSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid(raise_exception=True):
            return Response(
                {'msg': _("Password Changed Successfully")},
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class RequestResetPasswordView(viewsets.ModelViewSet):

    renderer_classes = [UserRenderer]
    serializer_class = serializers.RequestResetPasswordSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = serializers.RequestResetPasswordSerializer(data=request.data, context={'current_site': get_current_site(request)})
        if serializer.is_valid(raise_exception=True):
            return Response(
                {'msg': _("Password Reset link send. Please check your Email"), "code": "reset_link_sent_email"},
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UserResetPasswordView(viewsets.ModelViewSet):

    renderer_classes = [UserRenderer]
    serializer_class = serializers.UserResetPasswordSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        uidb64 = kwargs.get('uidb64')
        token = kwargs.get('token')
        serializer = serializers.UserResetPasswordSerializer(data=request.data, context={'uid': uidb64, 'token': token})
        if serializer.is_valid(raise_exception=True):
            return Response(
                {'msg': _("Password Reset Successfully")},
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LogoutView(viewsets.ModelViewSet):

    renderer_classes = [UserRenderer]
    serializer_class = serializers.LogoutSerializer
    http_method_names = ['post']
    lookup_field = 'public_id'

    def create(self, request, *args, **kwargs):
        serializer = serializers.LogoutSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(
                {'msg': _("Logout Successfully")},
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )