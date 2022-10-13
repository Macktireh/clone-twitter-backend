from django.db import models

from apps.utils.functions import list_to_queryset


class PostManager(models.Manager):
    
    def get_posts_like(self, me):
        from apps.post.models import Post
        
        posts = Post.objects.select_related('author').all()
        post_like = []
        for post in posts:
            for like in post.liked.all():
                if like == me: post_like.append(post)
        qs = list_to_queryset(model=Post, data=post_like)
        return qs
