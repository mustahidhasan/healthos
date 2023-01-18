from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from django.contrib import admin

from user.forms import UserChangeForm, UserCreationForm
from user.models import *


class CompanyAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'company_name'
    ]

class UsersAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        (None, {'fields': ('username', 'password', 'usr_email')}),
        (_('Profile info'), {'fields': ('first_name', 'last_name',  'gender', 'usr_profile_pic','user_type' )}),
        (_('Permissions'),
         {'fields': ('groups', 'is_verify', 'is_notification', 'is_message', 'is_active', 'is_staff', 'is_superuser',)}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')}
         ),
    )

    def user_type(self, obj):
        """
        get group, separate by comma, and display empty string if user has no group
        """
        return ','.join([g.name for g in obj.groups.all()]) if obj.groups.count() else ''
    
    list_display = (
        'username', 'usr_email','first_name', 'is_staff'
    )
    list_display_links = ('username',)
    list_filter = ['groups', ]
    search_fields = ('usr_email', 'first_name', 'last_name', 'username')
    ordering = ('usr_email',)
    readonly_fields = ('date_joined', 'last_login')

class UserCompanyManagerAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'company',
        'phn_cell',
        'is_primary_phone',

    ]


admin.site.register(User, UsersAdmin)

admin.site.register(Company, CompanyAdmin)
admin.site.register(UserCompanyManager, UserCompanyManagerAdmin)

