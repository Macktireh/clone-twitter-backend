from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.translation import gettext as _

from rest_framework import serializers

from apps.account.tokens import generate_token
from apps.utils.email import send_email_to_user


User = get_user_model()


class UserSignupSerializer(serializers.ModelSerializer):

    firstName = serializers.CharField(source='first_name')
    lastName = serializers.CharField(source='last_name')
    confirm_password = serializers.CharField(max_length=128, style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = [
            'email', 'firstName', 'lastName', 'password', 'confirm_password',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise serializers.ValidationError(
                _("Password and Confirm Password doesn't match")
            )
        return attrs

    def create(self, validate_data):
        validate_data.pop('confirm_password', None)
        return User.objects.create_user(**validate_data)


class UserActivationSerializer(serializers.Serializer):

    uidb64 = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)

    class Meta:
        fields = [
            'uidb64', 'token',
        ]

    def validate(self, attrs):
        uidb64 = attrs.get('uidb64')
        token = attrs.get('token')
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as e:
            user = None
        if user and generate_token.check_token(user, token):
            if not user.is_email_verified:
                user.is_email_verified = True
                user.save()
                send_email_to_user(
                    subject=f"{settings.DOMAIN_FRONTEND} - Your account has been successfully created and activated!", 
                    template_name='account/mail/activate_success.html', 
                    user=user, 
                    domain=settings.DOMAIN_FRONTEND
                )
        else:
            raise serializers.ValidationError(
                _("Token is not Valid or user is not exist")
            )
        return attrs


class UserLoginSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = [
            'email', 'password',
        ]


class UserChangePasswordSerializer(serializers.Serializer):

    password = serializers.CharField(max_length=128, style={'input_type': 'password'}, write_only=True)
    confirm_password = serializers.CharField(max_length=128, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = [
            'password', 'confirm_password'
        ]

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        user = self.context.get('user')
        if password != confirm_password:
            raise serializers.ValidationError(
                _("Password and Confirm Password doesn't match")
            )
        user.set_password(password)
        user.save()
        return attrs


class SendEmailResetPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        current_site = self.context.get('current_site')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            token = PasswordResetTokenGenerator().make_token(user)
            send_email_to_user(
                subject=f"Password reset on {current_site}",
                template_name='account/mail/send_email_reset_password.html',
                user=user,
                token=token,
                domain=settings.DOMAIN_FRONTEND
            )
        else:
            raise serializers.ValidationError(
                {"msg": _("The email address does not exist"), "code": "email_does_not_exist"}
            )
        return attrs


class UserResetPasswordSerializer(serializers.Serializer):

    password = serializers.CharField(max_length=128, style={'input_type': 'password'}, write_only=True)
    confirm_password = serializers.CharField(max_length=128, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = [
            'password', 'confirm_password'
        ]

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        uid = self.context.get('uid')
        token = self.context.get('token')
        if password != confirm_password:
            raise serializers.ValidationError(
                _("Password and Confirm Password doesn't match")
            )
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except Exception as e:
            user = None
        if user and PasswordResetTokenGenerator().check_token(user, token):
            user.set_password(password)
            user.save()
            send_email_to_user(
                subject=f"{settings.DOMAIN_FRONTEND} - Your password has been successfully changed!", 
                template_name='account/mail/password_rest_success.html', 
                user=user, 
                domain=settings.DOMAIN_FRONTEND
            )
        else:
            raise serializers.ValidationError(
                _("Token is not Valid or Expired")
            )
        return attrs


class UserSerializer(serializers.ModelSerializer):

    # firstName = serializers.CharField(source='first_name')
    # lastName = serializers.CharField(source='last_name')

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']
        extra_kwargs = {
            'id': {'read_only': True},
            'email': {'read_only': True},
        }