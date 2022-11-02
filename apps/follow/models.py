from django.db import models
from django.contrib.auth import get_user_model

from apps.follow.managers import FollowManager


User = get_user_model()

class Follow(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followers = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def number_of_following(self):
        return self.following.all()
    
    def number_of_follower(self):
        return self.follower.all()
    
    objects = FollowManager()
    
    def __str__(self):
        return f"{self.followers.first_name} followed by {self.following.first_name}"