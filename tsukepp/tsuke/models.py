from accounts.models import CustomUser
from django.db import models


class Tsuke(models.Model):
    """1回のツケ"""
    user = models.ForeignKey(CustomUser, verbose_name="ユーザ", on_delete=models.PROTECT)
    purchase_datetime = models.DateTimeField(verbose_name="購入日時", auto_now_add=True)
    amount = models.PositiveSmallIntegerField(verbose_name="金額")
    is_paid = models.BooleanField(verbose_name="清算済", default=False)
    note = models.CharField(verbose_name="メモ", max_length=50, blank=True)

    class Meta:
        verbose_name = "ツケ"
        verbose_name_plural = "ツケ"

    def __str__(self):
        return f"{self.amount}円{'（' + self.note + ')' if self.note else ''}"
