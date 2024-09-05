from django.db import models

from lms.models import NULLABLE
from users.models import User


class Payment(models.Model):
    session_id = models.CharField(max_length=255, verbose_name="ID сессии", **NULLABLE)

    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Сумма платежа", **NULLABLE
    )
    payment_url = models.URLField(
        max_length=400, verbose_name="Ссылка на платеж", **NULLABLE
    )
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, verbose_name="Пользователь", **NULLABLE
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"{self.user}; {self.amount}; {self.session_id}"
