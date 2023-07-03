from django.contrib import admin

# from django.contrib import admin
from django.contrib.admin import ModelAdmin
# Register your models here.
from .models import User, RequestedAttempts


class UserAdmin(ModelAdmin):
        list_display = ('id', 'email', 'username', 'first_name', 'last_name' ,'ip_address','blocked_user')
        list_filter = ('is_superuser',)
        fieldsets = [
                (None, {'fields': ('email', 'password',)}),
                ('Personal info', {'fields': ('first_name', 'last_name', 'username','ip_address','blocked_user',)}),
                ('Permissions', {'fields': ('is_superuser',)}),
        ]

        add_fieldsets = (
                (None, {
                        'classes': ('wide',),
                        'fields': ( 'is_student','ip_address','blocked_user'),
                }),
        )
        search_fields = ('username',)
        ordering = ('id',)
        filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(RequestedAttempts, ModelAdmin)