from django.contrib import admin
from django.utils.translation import gettext as _

from apps.comment.models import Comment, LikeComment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = ('comment_author', 'post_author', 'public_id', 'message', 'created', 'updated', 'is_updated',)

    def comment_author(self, instance):
        return f"{instance.author.get_full_name()}"

    def post_author(self, instance):
        return f"{instance.post.author.get_full_name()}"

    def public_id(self, instance):
        return f"{instance.post.public_id}"


@admin.register(LikeComment)
class LikeCommentAdmin(admin.ModelAdmin):

    list_display = ('like_author', 'comment_author', 'public_id', 'value', 'created',)

    def like_author(self, instance):
        return f"{instance.user.get_full_name()}"

    def comment_author(self, instance):
        return f"{instance.comment.author.get_full_name()}"

    def public_id(self, instance):
        return f"{instance.comment.public_id}"