from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.profiles.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = ('full_name', 'pseudo', 'bio', 'created', 'updated',)
    fieldsets = (
        (None, {'fields': ('user',)}),
        (_('Personal info'), {'fields': ('pseudo', 'bio', 'birth_date', 'profile_picture', 'cover_picture',)}),
        (_('Sorting'), {'fields': ('sort_id',)}),
    )
    search_fields = ('full_name', 'pseudo',)

    def full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"