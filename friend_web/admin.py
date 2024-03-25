from django.contrib import admin
from friend_web.models import *

# class GenderTypeInline(admin.TabularInline):
#     model = GenderType

# class GenderTypeAdmin(admin.ModelAdmin):
#     list_display = ["label", "user"]
#     pass
class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password', 'username')}),
        (('Personal info'), {'fields': ('first_name', 'last_name')}),
        (('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('username','email', 'first_name', 'last_name', 'is_staff', 'email_is_verified')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

class UserdataAdmin(admin.ModelAdmin):
    list_display = ["username", "bio", "headshot", "created_time",\
        "date_of_birth", "show_horoscope", "instagram_link", "facebook_link", "snapchat_link",\
            "inviteurl", "username_id"]
    # inlines = [GenderTypeInline]


class ConnectionAdmin(admin.ModelAdmin):

    list_display = ('inviter', 'invitee', 'id', 'date_established', 'closeness', 'nicknamechildtoparent', 'nicknameparenttochild', 'activated')
    pass

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Connection, ConnectionAdmin)
# admin.site.register(GenderType, GenderTypeAdmin)
admin.site.register(Userdata, UserdataAdmin)
