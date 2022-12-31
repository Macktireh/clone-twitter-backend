from django.contrib import admin
from django.utils.translation import gettext as _

from apps.post.models import Post, LikePost


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = ('author_post', 'body', 'number_of_like', 'created', 'updated', 'is_updated',)

    def author_post(self, instance):
        return f"{instance.author.get_full_name()}"

    def number_of_like(self, instance):
        return f"{instance.liked.all().count()}"


@admin.register(LikePost)
class LikePostAdmin(admin.ModelAdmin):

    list_display = ('like_author', 'post_author', 'public_id', 'value', 'created',)

    def like_author(self, instance):
        return f"{instance.user.get_full_name()}"

    def post_author(self, instance):
        return f"{instance.post.author.get_full_name()}"

    def public_id(self, instance):
        return f"{instance.post.public_id}"