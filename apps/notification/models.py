from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from apps.notification.managers import NotificationManager
from apps.post.models import LikePost, Post
from apps.comment.models import Comment, LikeComment
from apps.utils.functions import uid_generator


User = get_user_model()


class TypeNotifChoices(models.TextChoices):
    
    post = 'Add_Post', _('Add Post')
    like_post = 'Like_Post', _('Like Post')
    comment = 'Add_Comment', _('Add Comment')
    like_comment = 'Like_Comment', _('Like Comment')
    following = 'Follow_Or_Unfollow', _('Follow Unfollow')


class Notification(models.Model):
    
    public_id = models.CharField(max_length=64, unique=True, blank=True)
    type_notif = models.CharField(_('type_notif'), max_length=30, choices=TypeNotifChoices.choices)
    from_user = models.ForeignKey(User, related_name='notif_from', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='notif_to', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='notif_post', on_delete=models.CASCADE, blank=True, null=True)
    like_post = models.ForeignKey(LikePost, related_name='notif_like_post', on_delete=models.CASCADE, blank=True, null=True)
    comment_post = models.ForeignKey(Comment, related_name='notif_comment_post', on_delete=models.CASCADE, blank=True, null=True)
    like_comment = models.ForeignKey(LikeComment, related_name='notif_like_comment', on_delete=models.CASCADE, blank=True, null=True)
    seen = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    objects = NotificationManager()
    
    class Meta:
        ordering = ['-updated']
    
    def save(self, *args, **kwargs) -> None:
        if self.public_id == '' or self.public_id is None:
            self.public_id = uid_generator()
        super().save(*args, **kwargs)