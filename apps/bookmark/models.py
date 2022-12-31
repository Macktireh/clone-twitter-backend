from django.db import models
from django.contrib.auth import get_user_model

from apps.post.models import Post
from apps.bookmark.managers import BookmarkManager


User = get_user_model()


class Bookmark(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmark')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='bookmark')
    created = models.DateTimeField(auto_now_add=True)
    
    objects = BookmarkManager()

    def __str__(self):
        return self.user.get_full_name()