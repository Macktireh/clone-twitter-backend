import cloudinary

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from django_resized import ResizedImageField

from apps.post.managers import PostManager
from apps.utils.functions import rename_img_post, uid_generator


User = get_user_model()


class Post(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    public_id = models.CharField(max_length=64, unique=True, blank=True)
    body = models.TextField(blank=True, null=True)
    image = ResizedImageField(size=[500, 500], upload_to="cloneTwitter/media/post", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    liked = models.ManyToManyField(User, blank=True, default=None)
    bookmarks = models.ManyToManyField(User, blank=True, default=None, related_name='bookmarked_posts')
    is_updated = models.BooleanField(default=False)
    
    objects = PostManager()

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        ordering = ('-created',)

    def __str__(self):
        return f"Post-{self.id}-{self.author.get_full_name()}"

    @property
    def get_author(self):
        return f"{self.author.get_full_name()}"

    @property
    def number_of_like(self):
        return self.liked.all().count()

    def save(self, *args, **kwargs):
        if self.public_id == '' or self.public_id is None:
            self.public_id = uid_generator()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if len(str(self.image)) != 0 and self.image:
                cloudinary.uploader.destroy(str(self.image))
        super().delete(*args, **kwargs)


class LikeChoices(models.TextChoices):
    
    like = "Like", _('Like')
    unLike = "Unlike", _('Unlike')


class LikePost(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LikeChoices.choices, max_length=10)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('like post')
        verbose_name_plural = _('likes posts')
        ordering = ('-created',)

    def __str__(self):
        return f"Auteur: {self.user.get_full_name()} - {self.value} -  PostId: {self.post.id}"