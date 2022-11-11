import re

from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from rest_framework import serializers, validators

from apps.utils.response import response_messages


User = get_user_model()
res = response_messages('fr')


def email_validation(value):
    if not re.match(r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$", value):
        raise serializers.ValidationError(res["ENTER_A_VALID_EMAIL_ADDRESS"])
    if User.objects.filter(email__iexact=value).exists():
        raise serializers.ValidationError(res["USER_WITH_THIS_EMAIL_ADDRESS_ALREADY_EXISTS"])
    return value

def password_validation(value):
    if not re.match("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$", value):
        raise serializers.ValidationError(res["INVALID_PASSWORD"])
    return value