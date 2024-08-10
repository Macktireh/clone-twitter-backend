import cloudinary

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from apps.profiles.managers import ProfileManager
from apps.utils.functions import uid_generator


User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    pseudo = models.CharField(max_length=48, blank=True, unique=True)
    bio = models.CharField(max_length=360, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to="cloneTwitter/media/profile",
        default="https://res.cloudinary.com/doysjtoym/image/upload/v1/cloneTwitter/default/profilePic_hbvouc",
        blank=True,
        null=True,
    )
    cover_picture = models.ImageField(
        upload_to="cloneTwitter/media/cover",
        default="https://res.cloudinary.com/doysjtoym/image/upload/v1/cloneTwitter/default/coverPic_dbaax4",
        blank=True,
        null=True,
    )
    isUploadProfilePic = models.BooleanField(default=False)
    isUploadCoverPic = models.BooleanField(default=False)
    sort_id = models.IntegerField(default=9999, null=True)
    # following = models.ManyToManyField(User, blank=True, related_name='following')
    # follower = models.ManyToManyField(User, blank=True, related_name='follower')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = ProfileManager()

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def save(self, *args, **kwargs):
        if self.pseudo == "" or self.pseudo is None:
            self.pseudo = uid_generator()[:8]
        return super().save(*args, **kwargs)

    # def number_of_following(self):
    #     return self.following.all()

    def delete(self, *args, **kwargs):
        if len(str(self.profile_picture)) != 0 and self.profile_picture:
                cloudinary.uploader.destroy(str(self.profile_picture))
        if len(str(self.cover_picture)) != 0 and self.cover_picture:
                cloudinary.uploader.destroy(str(self.cover_picture))
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
        ordering = ("-created",)
