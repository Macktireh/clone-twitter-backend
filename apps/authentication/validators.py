import re

from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from rest_framework import serializers, validators


User = get_user_model()


def email_validation(value):
    if not re.match(r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$", value):
        raise serializers.ValidationError(
            _("Veuillez entrer une adresse email valide.")
        )
    if User.objects.filter(email__iexact=value).exists():
        raise serializers.ValidationError(
            _(f"Un utilisateur avec avec cette adresse email existe déjà.")
        )
    return value

def password_validation(value):
    if not re.match("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$", value):
        raise serializers.ValidationError(
            _("Le mot de passe doit contenir au moins 8 caractères, au moins une lettre majuscule et minuscule, un chiffre et un caractère spécial.")
        )
    return value