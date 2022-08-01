import re

from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from rest_framework import serializers


def password_validation(value):
    if not re.match("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$", value):
        raise serializers.ValidationError(
            _("The password must contain at least 8 characters, at least one upper and lower case letter, one number and one special character.")
        )
    return value