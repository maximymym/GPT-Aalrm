from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    This model is the primary user representation for the application.
    It's extended to include a `telegram_id` for potential bot integration.
    """
    telegram_id = models.BigIntegerField(
        verbose_name='Telegram ID',
        unique=True,
        null=True,
        blank=True,
        help_text='The unique user ID from Telegram, used for bot integration.'
    )

    def __str__(self):
        return self.username
