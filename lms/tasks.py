from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config import settings
from lms.models import Notifications


@shared_task
def send_notification_mail_on_course_update():
    four_hours = timezone.now() - timezone.timedelta(hours=4)
    notifications = Notifications.objects.filter(course__last_update__lt=four_hours)
    for notification in notifications:
        subscriptions = notification.course.subscriptions.all()
        subscriptions_emails = [subscription.user.email for subscription in subscriptions]

        send_mail(
            subject="Обновление курса!",
            message=f"Курс {notification.course.name} обновлен!",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=subscriptions_emails
        )

        notification.delete()
