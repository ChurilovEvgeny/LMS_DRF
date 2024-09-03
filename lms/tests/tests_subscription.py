from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from lms.models import Course, Lesson, Subscription
from users.models import User


# python manage.py test - запуск тестов
# python manage.py test lms.tests.tests_subscription - запуск конкретного файла
# coverage run --source='.' manage.py test - запуск проверки покрытия
# coverage report -m - получение отчета с пропущенными стрроками


class SubscriptionTestCaseAuthenticated(APITestCase):
    """Данные тесты описывают авторизованного пользователя и его подписки"""

    def setUp(self) -> None:
        self.user = User.objects.create(email="user@my.ru")
        self.course = Course.objects.create(name="Курс 1", owner=self.user)
        self.lesson = Lesson.objects.create(
            name="Урок 1", course=self.course, owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_subscription_str(self):
        Subscription.objects.create(user=self.user, course=self.course)

        subscription = Subscription.objects.get(
            user=self.user.pk, course=self.course.pk
        )
        self.assertEqual(
            str(subscription), f"{subscription.user}, {subscription.course}"
        )

    def test_subscription_create_and_delete(self):
        data = {
            "course": self.course.pk,
        }

        # Создание подписки
        response = self.client.post(reverse("lms:subscribe"), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        subscription = Subscription.objects.last()
        self.assertEqual(subscription.user, self.user)
        self.assertEqual(subscription.course, Course.objects.get(pk=data["course"]))

        # Удаление подписки (При условии запроса с теми же параметрами)
        response = self.client.post(reverse("lms:subscribe"), data=data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Subscription.objects.count(), 0)
