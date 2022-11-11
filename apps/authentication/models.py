from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from apps.authentication.managers import UserManager
from apps.utils.functions import uid_generator


class User(AbstractUser):

    username = None
    public_id = models.CharField(max_length=64, unique=True, null=False, blank=False)
    email = models.EmailField(
        _('email'),
        max_length=255,
        unique=True,
        help_text=_("Required to authenticate")
    )
    is_verified_email = models.BooleanField(
        _('email verified'), 
        default=False,
        help_text=_("Specifies whether the user should verify their email address.")
    )
    last_logout = models.DateTimeField(
        _('last date logout'), 
        blank=True, null=True,
        help_text=_("last date logout user")
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if self.public_id == '' or self.public_id is None:
            self.public_id = uid_generator()
        super().save(*args, **kwargs)
