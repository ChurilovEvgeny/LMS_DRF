from django.db import models

from utils.utils import generate_filename_course_preview, generate_filename_lesson_preview

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    name = models.CharField(max_length=150, verbose_name="Наименование курса")
    preview = models.ImageField(upload_to=generate_filename_course_preview, verbose_name="Аватар", **NULLABLE)
    description = models.TextField(verbose_name="Описание курса", **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    name = models.CharField(max_length=150, verbose_name="Наименование урока")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс", related_name="lessons")
    description = models.TextField(verbose_name="Описание урока", **NULLABLE)
    preview = models.ImageField(upload_to=generate_filename_lesson_preview, verbose_name="Аватар", **NULLABLE)
    video_url = models.URLField(verbose_name="Ссылка на видео", **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
