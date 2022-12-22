from django.contrib import admin

from apps.notification.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('updated', 'type_notif', '_from_user', '_to_user', 'seen', 'read',)
    list_editable = ('type_notif', 'seen', 'read',)
    list_filter = ('type_notif', 'seen', 'read',)
    ordering = ('-updated',)
    
    def _from_user(self, instance):
        return f"{instance.from_user.get_full_name()}"
    
    def _to_user(self, instance):
        return f"{instance.to_user.get_full_name()}"