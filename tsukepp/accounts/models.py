from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """拡張ユーザモデル"""

    class Meta:
        verbose_name = "ユーザ"
        verbose_name_plural = "ユーザ"
