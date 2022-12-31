from django.contrib import admin
from django.utils.translation import gettext as _

from apps.follow.models import Follow


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):

    list_display = ('created', '_followers', '_following', 'updated',)
    
    def _following(self, instance):
        return f"{instance.following.get_full_name()}"
    
    def _followers(self, instance):
        return f"{instance.followers.get_full_name()}"