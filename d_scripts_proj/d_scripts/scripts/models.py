from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

class Script(models.Model):
    """
    Represents a script in the catalog.
    """
    title = models.CharField(max_length=255, help_text="The title of the script.")
    description = models.TextField(help_text="A detailed description of the script.")
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.00)],
        help_text="The price of the script. Set to 0 for a free script."
    )
    video_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="URL to a demonstration video (e.g., YouTube)."
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Designates whether this script is visible in the catalog."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_free(self):
        """
        A property to determine if a script is free based on its price.
        """
        return self.price == 0.00

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class Order(models.Model):
    """
    Represents an order made by a user.
    """
    class OrderStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        COMPLETED = 'COMPLETED', 'Completed'
        FAILED = 'FAILED', 'Failed'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders',
        help_text="The user who placed the order."
    )
    status = models.CharField(
        max_length=10,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="The total amount of the order at the time of creation."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

    class Meta:
        ordering = ['-created_at']


class OrderItem(models.Model):
    """
    A through model connecting an Order to a Script.
    Represents a single script within an order.
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    script = models.ForeignKey(
        Script,
        on_delete=models.SET_NULL, # Keep order history even if script is deleted
        null=True,
        related_name='order_items'
    )
    price_at_purchase = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="The price of the script at the time the order was placed."
    )

    def __str__(self):
        return f"{self.script.title} in Order {self.order.id}"

    class Meta:
        unique_together = ('order', 'script') # A script can only be in an order once
