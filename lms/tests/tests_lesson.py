from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from lms.models import Course, Lesson
from users.models import User


# python manage.py test - запуск тестов
# python manage.py test lms.tests.tests_lesson - запуск конкретного файла
# coverage run --source='.' manage.py test - запуск проверки покрытия
# coverage report -m - получение отчета с пропущенными стрроками


class LessonTestCaseAuthenticated(APITestCase):
    """Данные тесты описывают авторизованного пользователя и его же доступ к своим же данным"""

    def setUp(self) -> None:
        self.user = User.objects.create(email="user@my.ru")
        self.course = Course.objects.create(name="Курс 1", owner=self.user)
        self.lesson = Lesson.objects.create(
            name="Урок 1", course=self.course, owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_str(self):
        lesson = Lesson.objects.get(pk=self.lesson.pk)
        self.assertEqual(str(lesson), lesson.name)

    def test_lesson_create(self):
        data = {
            "name": "Урок 2",
            "description": "Описание урока 2",
            "course": self.course.pk,
        }
        response = self.client.post(reverse("lms:lesson_create"), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        lesson = Lesson.objects.last()
        self.assertEqual(lesson.name, data["name"])
        self.assertEqual(lesson.description, data["description"])

    def test_lesson_list(self):
        response = self.client.get(reverse("lms:lesson_list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(
            data,
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.lesson.pk,
                        "name": self.lesson.name,
                        "description": None,
                        "preview": None,
                        "video_url": None,
                        "course": self.course.pk,
                        "owner": self.user.pk,
                    }
                ],
            },
        )

    def test_lesson_retrieve(self):
        response = self.client.get(
            reverse("lms:lesson_retrieve", args=(self.lesson.pk,))
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(
            data,
            {
                "id": self.lesson.pk,
                "name": self.lesson.name,
                "description": None,
                "preview": None,
                "video_url": None,
                "course": self.course.pk,
                "owner": self.user.pk,
            },
        )

    def test_lesson_update(self):
        data = {"name": "Урок 1 updated", "description": "Описание урока 1 updated"}
        response = self.client.patch(
            reverse("lms:lesson_update", args=(self.lesson.pk,)), data=data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        lesson = Lesson.objects.get(pk=self.lesson.pk)
        self.assertEqual(lesson.name, data["name"])
        self.assertEqual(lesson.description, data["description"])

    def test_lesson_delete(self):
        response = self.client.delete(
            reverse("lms:lesson_delete", args=(self.lesson.pk,))
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Lesson.objects.filter(pk=self.lesson.pk).exists())


class LessonTestCaseNotAuthenticated(APITestCase):
    """Данные тесты описывают НЕ авторизованного пользователя"""

    def setUp(self) -> None:
        self.user = User.objects.create(email="user@my.ru")
        self.course = Course.objects.create(name="Курс 1", owner=self.user)
        self.lesson = Lesson.objects.create(
            name="Урок 1", course=self.course, owner=self.user
        )
        # Пользователь НЕ авторизован! self.client.force_authenticate(user=self.user)

    def test_lesson_create(self):
        data = {"name": "Урок 2", "course": self.course.pk}
        response = self.client.post(reverse("lms:lesson_create"), data=data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_list(self):
        response = self.client.get(reverse("lms:lesson_list"))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_retrieve(self):
        response = self.client.get(
            reverse("lms:lesson_retrieve", args=(self.lesson.pk,))
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_update(self):
        data = {"name": "Урок 1 updated", "description": "Описание урока 1 updated"}
        response = self.client.patch(
            reverse("lms:lesson_update", args=(self.lesson.pk,)), data=data
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_delete(self):
        response = self.client.delete(
            reverse("lms:lesson_delete", args=(self.lesson.pk,))
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class LessonTestCaseAnotherAuthenticatedUser(APITestCase):
    """Данные тесты описывают авторизованного пользователя и его же доступ к ЧУЖИМ данным"""

    def setUp(self) -> None:
        self.user = User.objects.create(email="user@my.ru")
        self.user2 = User.objects.create(email="user2@my.ru")
        self.course = Course.objects.create(name="Курс 1", owner=self.user)
        self.lesson = Lesson.objects.create(
            name="Урок 1", course=self.course, owner=self.user
        )
        self.client.force_authenticate(user=self.user2)

    def test_lesson_list(self):
        response = self.client.get(reverse("lms:lesson_list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(
            data,
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.lesson.pk,
                        "name": self.lesson.name,
                        "description": None,
                        "preview": None,
                        "video_url": None,
                        "course": self.course.pk,
                        "owner": self.user.pk,
                    }
                ],
            },
        )

    def test_lesson_retrieve(self):
        response = self.client.get(
            reverse("lms:lesson_retrieve", args=(self.lesson.pk,))
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_update(self):
        data = {"name": "Урок 1 updated", "description": "Описание урока 1 updated"}
        response = self.client.patch(
            reverse("lms:lesson_update", args=(self.lesson.pk,)), data=data
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_delete(self):
        response = self.client.delete(
            reverse("lms:lesson_delete", args=(self.lesson.pk,))
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class LessonTestCaseModerAuthenticated(APITestCase):
    """Данные тесты описывают авторизованного модератора и его же доступ к данным"""

    def setUp(self) -> None:
        self.user = User.objects.create(email="user@my.ru")

        self.course = Course.objects.create(name="Курс 1", owner=self.user)
        self.lesson = Lesson.objects.create(
            name="Урок 1", course=self.course, owner=self.user
        )

        self.user_moder = User.objects.create(email="moder@my.ru")
        self.user_moder.groups.create(name="moders")
        self.client.force_authenticate(user=self.user_moder)

    def test_lesson_create(self):
        data = {
            "name": "Урок 2",
            "description": "Описание урока 2",
        }
        response = self.client.post(reverse("lms:lesson_create"), data=data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_list(self):
        response = self.client.get(reverse("lms:lesson_list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(
            data,
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.lesson.pk,
                        "name": self.lesson.name,
                        "description": None,
                        "preview": None,
                        "video_url": None,
                        "course": self.course.pk,
                        "owner": self.user.pk,
                    }
                ],
            },
        )

    def test_lesson_retrieve(self):
        response = self.client.get(
            reverse("lms:lesson_retrieve", args=(self.lesson.pk,))
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(
            data,
            {
                "id": self.lesson.pk,
                "name": self.lesson.name,
                "description": None,
                "preview": None,
                "video_url": None,
                "course": self.course.pk,
                "owner": self.user.pk,
            },
        )

    def test_lesson_update(self):
        data = {"name": "Курс 1 updated", "description": "Описание курса 1 updated"}
        response = self.client.put(
            reverse("lms:courses-detail", args=(self.course.pk,)), data=data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        course = Course.objects.get(pk=self.course.pk)
        self.assertEqual(course.name, data["name"])
        self.assertEqual(course.description, data["description"])

    def test_lesson_delete(self):
        response = self.client.delete(
            reverse("lms:lesson_delete", args=(self.lesson.pk,))
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
