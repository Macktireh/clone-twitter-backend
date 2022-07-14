from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from apps.account.models import User


class UserAdmin(BaseUserAdmin):
    # add_form = UserCreationForm
    # form = UserChangeForm
    model = User
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_email_verified', 'is_staff', 'is_superuser', 'date_joined',)
    list_filter = ('is_superuser', 'is_staff', 'is_active', 'is_email_verified', 'date_joined',)
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_email_verified', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('date_joined', 'last_login', 'last_logout',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'password1', 'password2', 'is_active', 'is_email_verified', 'is_staff')}
        ),
    )
    search_fields = ('email', 'first_name', 'last_name',)
    ordering = ('-date_joined',)


admin.site.register(User, UserAdmin)