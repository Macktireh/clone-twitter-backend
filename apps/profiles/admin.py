from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from apps.profiles.models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'pseudo', 'bio', 'birth_date',)
    # list_filter = ('gender',)
    fieldsets = (
        (None, {'fields': ('user', 'uid',)}),
        
        (_('Personal info'), {'fields': ('pseudo', 'bio', 'img_profile', 'img_bg', 'birth_date',)}),
        
        # (_('Location'), {'fields': ('adress', 'town', 'region', 'zipcode', 'country',),}),
        # (_('User description'), {'fields': ('description', 'bio')}),
        
        # (_('Social network'), {'fields': ('link_linkedin', 'link_gitthub', 'link_twitter', 'link_mysite',)}),
        (_('Following'), {'fields': ('following',)}),
    )

    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('first_name', 'last_name', 'email', 'password1', 'password2', 'is_active', 'is_email_verified', 'is_staff')}
    #     ),
    # )
    search_fields = ('full_name', 'pseudo',)
    
    def full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    
admin.site.register(Profile, ProfileAdmin)