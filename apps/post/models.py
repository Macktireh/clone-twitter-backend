from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

from apps.utils.function import rename_img_post


User = get_user_model()


class Post(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    uid = models.CharField(_("uid"), max_length=500, blank=True)
    message = models.TextField(_("message"), blank=True)
    img = models.ImageField(_("image"), upload_to=rename_img_post, blank=True, null=True)
    created = models.DateTimeField(_("created date"), auto_now_add=True)
    updated = models.DateTimeField(_("updated date"), auto_now=True)
    liked = models.ManyToManyField(User, blank=True, default=None)
    is_updated = models.BooleanField(_("is updated"), default=False)

    def __str__(self):
        return f"Post-{self.id}-{self.author.get_full_name()}"

    @property
    def get_author(self):
        return f"{self.author.get_full_name()}"

    @property
    def number_of_like(self):
        return self.liked.all().count()

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        ordering = ('-created',)


class LikePost(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    LIKE_CHOICES = (
        ('Like', 'Like'),
        ('Unlike', 'Unlike'),
    )
    value = models.CharField(choices=LIKE_CHOICES, max_length=10)
    created = models.DateTimeField(_("created date"), auto_now_add=True)

    class Meta:
        verbose_name = _('like post')
        verbose_name_plural = _('likes posts')
        ordering = ('-created',)

    def __str__(self):
        return f"Auteur: {self.user.get_full_name()} - {self.likes} -  PostId: {self.post.id}"


class Comment(models.Model):

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    message = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_updated = models.BooleanField(_("is updated"), default=False)

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')
        ordering = ('created',)

    def __str__(self):
        return f"Comment {self.id} - {self.author.get_full_name()}"

    @property
    def get_author(self):
        return f"{self.author.get_full_name()}"