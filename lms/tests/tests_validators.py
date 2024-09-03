from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from lms.models import Course, Lesson, Subscription
from users.models import User


# python manage.py test - запуск тестов
# python manage.py test lms.tests.tests_validators - запуск конкретного файла
# coverage run --source='.' manage.py test - запуск проверки покрытия
# coverage report -m - получение отчета с пропущенными стрроками


class ValidatorsTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(email="user@my.ru")
        self.client.force_authenticate(user=self.user)

    def test_course_validate_create(self):
        data = {
            "name": "Курс 2",
            "description": "https://youtube.com/watch",
        }
        response = self.client.post(reverse("lms:courses-list"), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 1)

    def test_course_invalidate_create_description(self):
        data = {
            "name": "Курс 2",
            "description": "https://youtube.com/watch https://rutube.com/watch",
        }
        response = self.client.post(reverse("lms:courses-list"), data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Course.objects.count(), 0)

        data = {
            "name": "Курс 2",
            "description": "https://youtube.com/watch http://rutube.com/watch",
        }
        response = self.client.post(reverse("lms:courses-list"), data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Course.objects.count(), 0)

        data = {
            "name": "Курс 2",
            "description": "http://rutube.com/watch",
        }
        response = self.client.post(reverse("lms:courses-list"), data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Course.objects.count(), 0)

    def test_lesson_validate_create(self):
        Course.objects.create(name="Курс 1")
        course = Course.objects.last()

        data = {
            "name": "Урок 1",
            "course": course.pk,
            "description": "https://youtube.com/watch",
            "video_url": "https://youtube.com/watch",
        }
        response = self.client.post(reverse("lms:lesson_create"), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 1)

    def test_lesson_invalidate_create_description(self):
        Course.objects.create(name="Курс 1")
        course = Course.objects.last()

        data = {
            "name": "Урок 1",
            "course": course.pk,
            "description": "https://youtube.com/watch https://rutube.com/watch",
        }
        response = self.client.post(reverse("lms:lesson_create"), data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Lesson.objects.count(), 0)

        data = {
            "name": "Урок 1",
            "course": course.pk,
            "description": "https://youtube.com/watch http://rutube.com/watch",
        }
        response = self.client.post(reverse("lms:lesson_create"), data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Lesson.objects.count(), 0)

        data = {
            "name": "Урок 1",
            "course": course.pk,
            "description": "http://rutube.com/watch",
        }
        response = self.client.post(reverse("lms:lesson_create"), data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_lesson_invalidate_create_video_url(self):
        Course.objects.create(name="Курс 1")
        course = Course.objects.last()

        data = {
            "name": "Урок 1",
            "course": course.pk,
            "video_url": "https://youtube.com/watch https://rutube.com/watch",
        }
        response = self.client.post(reverse("lms:lesson_create"), data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Lesson.objects.count(), 0)

        data = {
            "name": "Урок 1",
            "course": course.pk,
            "video_url": "https://rutube.com/watch",
        }
        response = self.client.post(reverse("lms:lesson_create"), data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Lesson.objects.count(), 0)

        data = {
            "name": "Урок 1",
            "course": course.pk,
            "video_url": "http://rutube.com/watch",
        }
        response = self.client.post(reverse("lms:lesson_create"), data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Lesson.objects.count(), 0)
