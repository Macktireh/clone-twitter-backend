from django.conf import settings
from google.auth.transport.requests import Request
from google.oauth2 import id_token
from requests_oauthlib import OAuth2Session
from rest_framework.exceptions import AuthenticationFailed

from apps.utils.response import res
from apps.authentication.models import User
from apps.authentication.tokens import get_tokens_for_user


class GoogleLogin:
    GOOGLE_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
    REDIRECT_URI = (
        settings.DOMAIN_FRONTEND
        if settings.DOMAIN_FRONTEND.endswith("/")
        else f"{settings.DOMAIN_FRONTEND}/"
    )
    SCOPES = [
        "openid",
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
    ]

    @staticmethod
    def echange_code_for_token(code):
        try:
            oauth2_session = OAuth2Session(
                client_id=settings.GOOGLE_CLIENT_ID,
                redirect_uri=GoogleLogin.REDIRECT_URI,
                scope=GoogleLogin.SCOPES,
            )

            token = oauth2_session.fetch_token(
                token_url=GoogleLogin.GOOGLE_TOKEN_ENDPOINT,
                client_secret=settings.GOOGLE_CLIENT_SECRET,
                code=code,
            )

            return token["id_token"]
        except Exception:
            raise Exception("Invalid code received, please try again")

    @staticmethod
    def validate(code):
        try:
            token = GoogleLogin.echange_code_for_token(code)
            id_info = id_token.verify_oauth2_token(
                id_token=token, request=Request(), audience=settings.GOOGLE_CLIENT_ID
            )
            if "accounts.google.com" in id_info["iss"]:
                return id_info
        except Exception:
            return "Invalid Token"


def register_user_with_social_account(auth_provider, email, first_name, last_name):
    print()
    print("register_user_with_social_account", auth_provider, email, first_name, last_name)
    print()
    try:
        user, created = User.objects.get_or_create(
            email=email,
            first_name=first_name,
            last_name=last_name,
            auth_provider=auth_provider,
        )
    except Exception:
        raise AuthenticationFailed(f"Get OR Create User: {email} {first_name} {last_name} {auth_provider}.")

    if created:
        user.is_verified_email = True
        # user.auth_provider = auth_provider
        user.save()
    # else:
    #     if user.auth_provider != auth_provider:
    #         raise AuthenticationFailed(
    #             f"Please use your {user.auth_provider} account to login."
    #         )

    token = get_tokens_for_user(user)
    return {"message": res["LOGIN_SUCCESS"], "token": token}
