from django.contrib import admin
from .models import Script, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    """
    Allows editing OrderItems directly within the Order admin page.
    This provides a convenient way to see which scripts are part of an order.
    """
    model = OrderItem
    extra = 0 # Don't show extra empty forms
    readonly_fields = ('script', 'price_at_purchase') # These should not be changed after order creation

@admin.register(Script)
class ScriptAdmin(admin.ModelAdmin):
    """
    Configuration for the Script model in the Django admin interface.
    """
    list_display = ('title', 'price', 'is_free', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('is_free', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'price', 'is_active')
        }),
        ('Content', {
            'fields': ('video_url',)
        }),
        ('Auto-generated', {
            'fields': ('is_free', 'created_at', 'updated_at')
        }),
    )

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Configuration for the Order model in the Django admin interface.
    """
    list_display = ('id', 'user', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('user', 'total_amount', 'created_at')
    inlines = [OrderItemInline] # Show order items in the order view

    def has_add_permission(self, request):
        # Orders should be created programmatically, not manually in admin.
        return False
