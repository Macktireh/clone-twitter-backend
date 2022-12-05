from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.translation import gettext as _
from django.utils import timezone

from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from apps.authentication.tokens import TokenGenerator
from apps.authentication.validators import email_validation, password_validation
from apps.utils.email import send_email
from apps.utils.response import error_messages, response_messages


User = get_user_model()
res = response_messages('fr')


class SignupSerializer(serializers.ModelSerializer):

    email = serializers.CharField(
        validators=[email_validation],
        error_messages={
            "blank": error_messages('blank', 'fr', 'email'),
            "required": error_messages('required', 'fr', 'email'),
        },
    )
    firstName = serializers.CharField(
        source='first_name', 
        error_messages={
            "blank": error_messages('blank', 'fr', 'Prénom'),
            "required": error_messages('required', 'fr', 'Prénom'),
        },
    )
    lastName = serializers.CharField(
        source='last_name', 
        error_messages={
            "blank": error_messages('blank', 'fr', 'Nom'),
            "required": error_messages('required', 'fr', 'Nom'),
        },
    )
    password = serializers.CharField(
        validators=[password_validation], 
        write_only=True, 
        error_messages={
            "blank": error_messages('blank', 'fr', 'Mot de passe'),
            "required": error_messages('required', 'fr', 'Mot de passe'),
        },
    )
    confirmPassword = serializers.CharField(
        max_length=128, 
        style={'input_type': 'password'}, 
        write_only=True,
        error_messages={
            "blank": error_messages('blank', 'fr', 'Confirmation mot de passe'),
            "required": error_messages('required', 'fr', 'Confirmation mot de passe'),
        },
    )

    class Meta:
        model = User
        fields = ['email', 'firstName', 'lastName', 'password', 'confirmPassword',]

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirmPassword')
        if password and confirm_password and password != confirm_password:
            raise serializers.ValidationError(res["PASSWORD_AND_PASSWORD_CONFIRM_NOT_MATCH"])
        return attrs

    def create(self, validate_data):
        validate_data.pop('confirmPassword', None)
        return User.objects.create_user(**validate_data)


class ActivationSerializer(serializers.Serializer):

    uidb64 = serializers.CharField(write_only=True)
    token = serializers.CharField(write_only=True)

    class Meta:
        fields = ['uidb64', 'token',]

    def validate(self, attrs):
        uidb64 = attrs.get('uidb64')
        token = attrs.get('token')
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as e:
            user = None
        if user and TokenGenerator().check_token(user, token):
            if not user.is_verified_email:
                user.is_verified_email = True
                user.save()
                send_email(
                    subject=f"{settings.DOMAIN_FRONTEND} - Your account has been successfully created and activated!", 
                    template_name='authentication/mail/activate_success.html', 
                    user=user, 
                    domain=settings.DOMAIN_FRONTEND
                )
        else:
            raise serializers.ValidationError(res["TOKEN_IS_NOT_VALID_OR_HAS_EXPIRED"])
        return attrs


class LoginSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        max_length=255,
        error_messages={
            "blank": error_messages('blank', 'fr', 'email'),
            "required": error_messages('required', 'fr', 'email'),
        },
    )
    password = serializers.CharField(
        error_messages={
            "blank": error_messages('blank', 'fr', 'Mot de passe'),
            "required": error_messages('required', 'fr', 'Mot de passe'),
        },
    )

    class Meta:
        model = User
        fields = ['email', 'password',]


class UserChangePasswordSerializer(serializers.Serializer):

    password = serializers.CharField(
        max_length=128, 
        style={'input_type': 'password'}, 
        write_only=True, 
        validators=[password_validation],
        error_messages={
            "blank": error_messages('blank', 'fr', 'Mot de passe'),
            "required": error_messages('required', 'fr', 'Mot de passe'),
        },
    )
    confirm_password = serializers.CharField(
        max_length=128, 
        style={'input_type': 'password'}, 
        write_only=True,
        error_messages={
            "blank": error_messages('blank', 'fr', 'Confirmation mot de passe'),
            "required": error_messages('required', 'fr', 'Confirmation mot de passe'),
        },
    )

    class Meta:
        fields = ['password', 'confirm_password']

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        user = self.context.get('user')
        if password != confirm_password:
            raise serializers.ValidationError(res["PASSWORD_AND_PASSWORD_CONFIRM_NOT_MATCH"])
        user.set_password(password)
        user.save()
        return attrs


class RequestResetPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField(
        max_length=255,
        error_messages={
            "blank": error_messages('blank', 'fr', 'email'),
            "required": error_messages('required', 'fr', 'email'),
        },
    )

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        current_site = self.context.get('current_site')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            token = PasswordResetTokenGenerator().make_token(user)
            send_email(
                subject=f"Réinitialisation du mot de passe sur {current_site}",
                template_name='authentication/mail/send_email_reset_password.html',
                user=user,
                token=token,
                domain=settings.DOMAIN_FRONTEND
            )
        else:
            raise serializers.ValidationError(res["EMAIL_ADDRESS_DOES_NOT_EXIST"])
        return attrs


class UserResetPasswordSerializer(serializers.Serializer):

    password = serializers.CharField(
        max_length=128, 
        style={'input_type': 'password'}, 
        write_only=True, 
        validators=[password_validation],
        error_messages={
            "blank": error_messages('blank', 'fr', 'Mot de passe'),
            "required": error_messages('required', 'fr', 'Mot de passe'),
        },
    )
    confirm_password = serializers.CharField(
        max_length=128, 
        style={'input_type': 'password'}, 
        write_only=True,
        error_messages={
            "blank": error_messages('blank', 'fr', 'Comfirmation mot de passe'),
            "required": error_messages('required', 'fr', 'Confirmation mot de passe'),
        },
    )

    class Meta:
        fields = ['password', 'confirm_password']

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        uid = self.context.get('uid')
        token = self.context.get('token')
        if password != confirm_password:
            raise serializers.ValidationError(res["PASSWORD_AND_PASSWORD_CONFIRM_NOT_MATCH"])
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except Exception as e:
            user = None
        if user and PasswordResetTokenGenerator().check_token(user, token):
            user.set_password(password)
            user.save()
            send_email(
                subject=f"{settings.DOMAIN_FRONTEND} - Votre mot de passe a été changé avec succès !", 
                template_name='authentication/mail/password_rest_success.html', 
                user=user, 
                domain=settings.DOMAIN_FRONTEND
            )
        else:
            raise serializers.ValidationError(res["TOKEN_IS_NOT_VALID_OR_HAS_EXPIRED"])
        return attrs


class LogoutSerializer(serializers.Serializer):
    
    public_id = serializers.CharField(
        write_only=True,
        error_messages={
            "blank": "Le champ public_id ne doit pas être vide.",
            "required": "Le champ public_id est obligatoire.",
        },
    )
    refresh = serializers.CharField(
        write_only=True,
        error_messages={
            "blank": "Le champ refresh ne doit pas être vide.",
            "required": "Le champ refresh est obligatoire.",
        },
    )
    
    class Meta:
        fields = ['public_id', 'refresh']
        
    def validate(self, attrs):
        public_id = attrs.get('public_id', None)
        refresh = attrs.get('refresh', None)
        if not public_id or not refresh:
            raise serializers.ValidationError(
                _("Les champs public_id et refresh sont obligatoire.")
            )
        self.public_id = public_id
        self.refresh = refresh
        return attrs
    
    def save(self, attrs):
        try:
            RefreshToken(self.refresh).blacklist()
        except TokenError:
            self.fail("bad refresh token")
        try:
            user = User.objects.get(public_id=self.public_id)
            user.last_logout = timezone.now()
            user.save()
            return attrs
        except:
            raise serializers.ValidationError(res["USER_DOES_NOT_EXIST"])