from django.db import models
from django.utils import timezone

from utils.utils import (
    generate_filename_course_preview,
    generate_filename_lesson_preview,
)

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    name = models.CharField(max_length=150, verbose_name="Наименование курса")
    preview = models.ImageField(
        upload_to=generate_filename_course_preview, verbose_name="Аватар", **NULLABLE
    )
    description = models.TextField(verbose_name="Описание курса", **NULLABLE)

    owner = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="courses", **NULLABLE
    )

    last_update = models.DateTimeField(verbose_name='Последняя дата/время обновления курса', auto_now=True)

    def update_last_update(self):
        self.last_update = timezone.now()
        self.save()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    name = models.CharField(max_length=150, verbose_name="Наименование урока")
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="Курс", related_name="lessons"
    )
    description = models.TextField(verbose_name="Описание урока", **NULLABLE)
    preview = models.ImageField(
        upload_to=generate_filename_lesson_preview, verbose_name="Аватар", **NULLABLE
    )
    video_url = models.URLField(verbose_name="Ссылка на видео", **NULLABLE)

    owner = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="lessons", **NULLABLE
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Subscription(models.Model):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        verbose_name="пользователь",
        related_name="subscriptions",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="курс",
        related_name="subscriptions",
    )

    @staticmethod
    def is_exist(user_pk: int, course_pk: int) -> bool:
        return Subscription.objects.filter(
            user_id=user_pk, course_id=course_pk
        ).exists()

    def __str__(self):
        return f"{self.user}, {self.course}"

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"


class Notifications(models.Model):
    course = models.OneToOneField(
        Course,
        on_delete=models.CASCADE,
        verbose_name="курс",
        related_name="notifications",
    )

    def __str__(self):
        return f"{self.course}"

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"
