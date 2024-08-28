from django.apps import apps
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from lms.models import Course, Lesson
from utils.utils import generate_filename_user_avatar


# Пример команды для создания суперпользователя (Обязательно через --email)
# python manage.py createsuperuser --email test@test.ru
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email должен быть указан")
        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        email = GlobalUserModel.normalize_username(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    objects = UserManager()

    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    phone_number = PhoneNumberField(
        verbose_name="Номер телефона", blank=True, null=True
    )
    avatar = models.ImageField(
        upload_to=generate_filename_user_avatar,
        verbose_name="Аватар",
        blank=True,
        null=True,
    )
    city = models.CharField(max_length=150, verbose_name="Город", blank=True, null=True)

    token = models.CharField(
        max_length=255, verbose_name="token", blank=True, null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email

    def get_email(self):
        return self.email


class Payment(models.Model):
    PAYMENT_CASH = "CASH"
    PAYMENT_CARD = "CARD"

    PAYMENT_METHOD_CHOICES = {
        PAYMENT_CASH: "Наличные",
        PAYMENT_CARD: "Перевод",
    }
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="payments",
    )
    date = models.DateTimeField(verbose_name="Дата оплаты")
    payment_course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Оплаченный курс",
        related_name="courses",
        blank=True,
        null=True,
    )
    payment_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        verbose_name="Оплаченный урок",
        related_name="lessons",
        blank=True,
        null=True,
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Сумма оплаты"
    )
    payment_method = models.CharField(
        max_length=30,
        verbose_name="Метод оплаты",
        choices=PAYMENT_METHOD_CHOICES,
        default=PAYMENT_CARD,
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return self.user
