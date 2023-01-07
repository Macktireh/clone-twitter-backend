from django.contrib import admin

from apps.bookmark.models import Bookmark


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):

    list_display = ('_user', 'post', 'created',)

    def _user(self, instance):
        return f"{instance.user.get_full_name()}"

    # def _post(self, instance):
    #     return f"{instance.liked.all().count()}"