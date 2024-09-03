import datetime

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from lms.models import Lesson, Course
from users.models import User, Payment


# python manage.py test - запуск тестов
# python manage.py test users.tests.tests_payment - запуск конкретного файла
# coverage run --source='.' manage.py test - запуск проверки покрытия
# coverage report -m - получение отчета с пропущенными стрроками


class PaymentTestCase(APITestCase):

    def setUp(self) -> None:
        def fill(fill_class, data):
            data_for_create = []
            for d in data:
                data_for_create.append(fill_class(**d))
            fill_class.objects.bulk_create(data_for_create)

            # Добавим курсы

        courses = [{"pk": 600011, "name": "Курс 11"}, {"pk": 600012, "name": "Курс 12"}]
        fill(Course, courses)

        # Добавим уроки
        lessons = [
            {"pk": 700011, "name": "Урок 111", "course": Course.objects.get(pk=600011)},
            {"pk": 700012, "name": "Урок 112", "course": Course.objects.get(pk=600012)},
        ]
        fill(Lesson, lessons)

        # Добавим пользователей
        users = [
            {"pk": 800011, "email": "user1@my.ru"},
            {"pk": 800012, "email": "user2@my.ru"},
        ]
        fill(User, users)

        # Добавим информацию об оплате
        d1 = datetime.datetime(1997, 10, 19, 12, 0, 0)
        d2 = datetime.datetime(1998, 10, 19, 12, 0, 0)

        self.payments = [
            {
                "pk": 900011,
                "user": User.objects.get(pk=800011),
                "date": d1,
                "payment_course": Course.objects.get(pk=600011),
                "amount": "1000",
                "payment_method": Payment.PAYMENT_CASH,
            },
            {
                "pk": 900012,
                "user": User.objects.get(pk=800012),
                "date": d2,
                "payment_lesson": Lesson.objects.get(pk=700012),
                "amount": "500",
                "payment_method": Payment.PAYMENT_CARD,
            },
        ]
        fill(Payment, self.payments)
        self.client.force_authenticate(user=User.objects.get(email="user1@my.ru"))

    def test_payment_str(self):
        payment = Payment.objects.get(pk=900011)
        self.assertEqual(str(payment), str(payment.user))

    def test_payment_list(self):
        response = self.client.get(reverse("users:payment_list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertEqual(data[0]["id"], self.payments[0]["pk"])
        self.assertEqual(data[0]["payment_method"], self.payments[0]["payment_method"])

        self.assertEqual(data[1]["id"], self.payments[1]["pk"])
        self.assertEqual(data[1]["payment_method"], self.payments[1]["payment_method"])


