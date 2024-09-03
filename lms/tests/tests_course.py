from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from lms.models import Course, Lesson
from users.models import User


# python manage.py test - запуск тестов
# coverage run --source='.' manage.py test - запуск проверки покрытия
# coverage report -m - получение отчета с пропущенными стрроками


class CourseTestCaseAuthenticated(APITestCase):
    """Данные тесты описывают авторизованного пользователя и его же доступ к своим же данным"""

    def setUp(self) -> None:
        self.user = User.objects.create(email="user@my.ru")
        self.course = Course.objects.create(name="Курс 1", owner=self.user)
        self.lesson = Lesson.objects.create(
            name="Урок 1", course=self.course, owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_course_str(self):
        course = Course.objects.get(pk=self.course.pk)
        self.assertEqual(str(course), course.name)

    def test_course_create(self):
        data = {
            "name": "Курс 2",
            "description": "Описание курса 2",
        }
        response = self.client.post(reverse("lms:courses-list"), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        course = Course.objects.last()
        self.assertEqual(course.name, data["name"])
        self.assertEqual(course.description, data["description"])

    def test_course_list(self):
        response = self.client.get(reverse("lms:courses-list"))

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
                        "pk": self.course.pk,
                        "name": self.course.name,
                        "preview": None,
                        "description": None,
                        "lessons_count": 1,
                        "is_subscribed": False,
                        "lessons": [
                            {
                                "id": self.lesson.pk,
                                "name": self.lesson.name,
                                "description": None,
                                "preview": None,
                                "video_url": None,
                                "course": self.lesson.course.pk,
                                "owner": self.user.pk,
                            }
                        ],
                    }
                ],
            },
        )

    def test_course_retrieve(self):
        response = self.client.get(
            reverse("lms:courses-detail", args=(self.course.pk,))
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(
            data,
            {
                "pk": self.course.pk,
                "name": self.course.name,
                "preview": None,
                "description": None,
                "lessons_count": 1,
                "is_subscribed": False,
                "lessons": [
                    {
                        "id": self.lesson.pk,
                        "name": self.lesson.name,
                        "description": None,
                        "preview": None,
                        "video_url": None,
                        "course": self.lesson.course.pk,
                        "owner": self.user.pk,
                    }
                ],
            },
        )

    def test_course_update(self):
        data = {"name": "Курс 1 updated", "description": "Описание курса 1 updated"}
        response = self.client.put(
            reverse("lms:courses-detail", args=(self.course.pk,)), data=data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        course = Course.objects.get(pk=self.course.pk)
        self.assertEqual(course.name, data["name"])
        self.assertEqual(course.description, data["description"])

    def test_course_delete(self):
        response = self.client.delete(
            reverse("lms:courses-detail", args=(self.course.pk,))
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Course.objects.filter(pk=self.course.pk).exists())


class CourseTestCaseNotAuthenticated(APITestCase):
    """Данные тесты описывают НЕ авторизованного пользователя"""

    def setUp(self) -> None:
        self.user = User.objects.create(email="user@my.ru")
        self.course = Course.objects.create(name="Курс 1", owner=self.user)
        self.lesson = Lesson.objects.create(
            name="Урок 1", course=self.course, owner=self.user
        )
        # Пользователь НЕ авторизован! self.client.force_authenticate(user=self.user)

    def test_course_create(self):
        data = {
            "name": "Курс 2",
        }
        response = self.client.post(reverse("lms:courses-list"), data=data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_course_list(self):
        response = self.client.get(reverse("lms:courses-list"))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_course_retrieve(self):
        response = self.client.get(
            reverse("lms:courses-detail", args=(self.course.pk,))
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_course_update(self):
        data = {"name": "Курс 1 updated", "description": "Описание курса 1 updated"}
        response = self.client.put(
            reverse("lms:courses-detail", args=(self.course.pk,)), data=data
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_course_delete(self):
        response = self.client.delete(
            reverse("lms:courses-detail", args=(self.course.pk,))
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CourseTestCaseAnotherAuthenticatedUser(APITestCase):
    """Данные тесты описывают авторизованного пользователя и его же доступ к ЧУЖИМ данным"""

    def setUp(self) -> None:
        self.user = User.objects.create(email="user@my.ru")
        self.user2 = User.objects.create(email="user2@my.ru")
        self.course = Course.objects.create(name="Курс 1", owner=self.user)
        self.lesson = Lesson.objects.create(
            name="Урок 1", course=self.course, owner=self.user
        )
        self.client.force_authenticate(user=self.user2)

    def test_course_list(self):
        response = self.client.get(reverse("lms:courses-list"))

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
                        "pk": self.course.pk,
                        "name": self.course.name,
                        "preview": None,
                        "description": None,
                        "lessons_count": 1,
                        "is_subscribed": False,
                        "lessons": [
                            {
                                "id": self.lesson.pk,
                                "name": self.lesson.name,
                                "description": None,
                                "preview": None,
                                "video_url": None,
                                "course": self.lesson.course.pk,
                                "owner": self.user.pk,
                            }
                        ],
                    }
                ],
            },
        )

    def test_course_retrieve(self):
        response = self.client.get(
            reverse("lms:courses-detail", args=(self.course.pk,))
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_course_update(self):
        data = {"name": "Курс 1 updated", "description": "Описание курса 1 updated"}
        response = self.client.put(
            reverse("lms:courses-detail", args=(self.course.pk,)), data=data
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_course_delete(self):
        response = self.client.delete(
            reverse("lms:courses-detail", args=(self.course.pk,))
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CourseTestCaseModerAuthenticated(APITestCase):
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

    def test_course_create(self):
        data = {
            "name": "Курс 2",
            "description": "Описание курса 2",
        }
        response = self.client.post(reverse("lms:courses-list"), data=data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_course_list(self):
        response = self.client.get(reverse("lms:courses-list"))

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
                        "pk": self.course.pk,
                        "name": self.course.name,
                        "preview": None,
                        "description": None,
                        "lessons_count": 1,
                        "is_subscribed": False,
                        "lessons": [
                            {
                                "id": self.lesson.pk,
                                "name": self.lesson.name,
                                "description": None,
                                "preview": None,
                                "video_url": None,
                                "course": self.lesson.course.pk,
                                "owner": self.user.pk,
                            }
                        ],
                    }
                ],
            },
        )

    def test_course_retrieve(self):
        response = self.client.get(
            reverse("lms:courses-detail", args=(self.course.pk,))
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertEqual(
            data,
            {
                "pk": self.course.pk,
                "name": self.course.name,
                "preview": None,
                "description": None,
                "lessons_count": 1,
                "is_subscribed": False,
                "lessons": [
                    {
                        "id": self.lesson.pk,
                        "name": self.lesson.name,
                        "description": None,
                        "preview": None,
                        "video_url": None,
                        "course": self.lesson.course.pk,
                        "owner": self.user.pk,
                    }
                ],
            },
        )

    def test_course_update(self):
        data = {"name": "Курс 1 updated", "description": "Описание курса 1 updated"}
        response = self.client.put(
            reverse("lms:courses-detail", args=(self.course.pk,)), data=data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        course = Course.objects.get(pk=self.course.pk)
        self.assertEqual(course.name, data["name"])
        self.assertEqual(course.description, data["description"])

    def test_course_delete(self):
        response = self.client.delete(
            reverse("lms:courses-detail", args=(self.course.pk,))
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
