from django.contrib import admin

from apps.notification.models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('updated', 'type_notif', 'from_user', 'to_user', 'seen', 'read',)
    list_editable = ('type_notif', 'seen', 'read',)
    list_filter = ('type_notif', 'seen', 'read',)
    ordering = ('-updated',)