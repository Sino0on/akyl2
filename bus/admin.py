from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Bus, BusRoute, BusEntry


class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {"fields": ("bus",)}),
    )
    list_display = BaseUserAdmin.list_display + ("bus",)
    list_filter = BaseUserAdmin.list_filter + ("bus",)

admin.site.register(User, UserAdmin)
admin.site.register(Bus)
admin.site.register(BusRoute)
admin.site.register(BusEntry)
