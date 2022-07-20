from django.contrib import admin
from django.utils.translation import gettext as _

from apps.post.models import Post, LikePost, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ('author_post', 'message', 'number_of_like', 'created', 'updated', 'is_updated',)
    
    def author_post(self, instance):
        return f"{instance.author.get_full_name()}"
    
    def number_of_like(self, instance):
        return f"{instance.liked.all().count()}"

admin.site.register(Post, PostAdmin)


class LikePostAdmin(admin.ModelAdmin):
    list_display = ('like_author', 'post_author', 'post_id', 'value', 'created',)
    
    def like_author(self, instance):
        return f"{instance.user.get_full_name()}"
    
    def post_author(self, instance):
        return f"{instance.post.author.get_full_name()}"
    
    def post_id(self, instance):
        return f"{instance.post.id}"

admin.site.register(LikePost, LikePostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_author', 'post_author', 'post_id', 'message', 'created', 'updated', 'is_updated',)
    
    def comment_author(self, instance):
        return f"{instance.author.get_full_name()}"
    
    def post_author(self, instance):
        return f"{instance.post.author.get_full_name()}"
    
    def post_id(self, instance):
        return f"{instance.post.id}"

admin.site.register(Comment, CommentAdmin)
