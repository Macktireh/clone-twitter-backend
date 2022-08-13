from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from apps.utils.function import rename_img_profile, uid_gerator


User = get_user_model()


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    uid = models.CharField(_('uid'), max_length=500, blank=True)
    pseudo = models.CharField(_('pseudo'), max_length=48, blank=True, unique=True)
    bio = models.CharField(_('bio'), max_length=360, blank=True)
    birth_date = models.DateField(_('birth date'), null=True, blank=True)
    profile_picture = models.ImageField(_('profile picture'), upload_to=rename_img_profile, default='default/profilePic.jpg', blank=True, null=True)
    cover_picture = models.ImageField(_('cover picture'), upload_to=rename_img_profile, default='default/coverPic.jpg', blank=True, null=True)
    following = models.ManyToManyField(User, blank=True, related_name='following')    
    updated = models.DateTimeField(_('update date'), auto_now=True)
    created = models.DateTimeField(_('created date'), auto_now_add=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def save(self, *args, **kwargs):
        if self.uid == '':
            self.uid = uid_gerator(self.user.id) + str(self.user.id) + uid_gerator(self.user.id)[:8]
        if self.pseudo == '':
            if self.user.first_name is not None or self.user.first_name != '':
                self.pseudo = uid_gerator(self.user.id)[:8] + str(self.user.id) + uid_gerator(self.user.id)[:8]
        return super().save(*args, **kwargs)

    def get_friends(self):
        return self.friends.all()

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')
        ordering = ('-created',)
