from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config import settings
from lms.models import Notifications
from users.models import User


@shared_task
def deactivate_unactive_users():
    """Данная задача проверяет активность пользователей
    Если пользователь был активен последний раз более 30 дней назад,
    то его профиль переводится в неактивный"""
    month = timezone.now() - timezone.timedelta(days=30)
    old_users = User.objects.filter(last_login__lt=month)
    for user in old_users:
        user.is_active = False
        user.save()
