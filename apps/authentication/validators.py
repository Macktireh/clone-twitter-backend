import re

from django.contrib.auth import get_user_model

from rest_framework import serializers

from apps.utils.response import res


User = get_user_model()


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