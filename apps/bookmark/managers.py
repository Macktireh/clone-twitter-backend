from django.db import models


class BookmarkManager(models.Manager):
    
    def getBookmarksByUser(self, user):
        
        from apps.bookmark.models import Bookmark
        return Bookmark.objects.filter(user=user)
    
    def getBookmarksByPost(self, post):
        
        from apps.bookmark.models import Bookmark
        return Bookmark.objects.filter(post=post)
