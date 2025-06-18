from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.

class CustomUserAdmin(UserAdmin):
    """
    Configuration for the custom User model in the Django admin interface.
    """
    model = User
    # Add custom fields to the list displays
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'telegram_id')
    # Add custom fields to fieldsets for editing
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('telegram_id',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('telegram_id',)}),
    )


admin.site.register(User, CustomUserAdmin)
