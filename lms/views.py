from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    get_object_or_404,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from lms.models import Course, Lesson, Subscription, Notifications
from lms.paginators import CustomPagePagination
from lms.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModer, IsOwner


class CourseViewSet(ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CustomPagePagination

    def perform_create(self, serializer):
        course = serializer.save(owner=self.request.user)
        course.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [~IsModer, IsAuthenticated]
        elif self.action == "destroy":
            self.permission_classes = [
                IsAuthenticated,
                ~IsModer | IsOwner,
            ]
        elif self.action in ["partial_update", "update", "retrieve"]:
            self.permission_classes = [IsAuthenticated, IsModer | IsOwner]
        return super().get_permissions()

    def perform_update(self, serializer):
        course = serializer.save()
        Notifications.objects.get_or_create(course=course)


class LessonCreateAPIView(CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [~IsModer, IsAuthenticated]

    def perform_create(self, serializer):
        lesson = serializer.save(owner=self.request.user)
        lesson.save()


class LessonListAPIView(ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = CustomPagePagination


class LessonRetrieveAPIView(RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [
        IsAuthenticated,
        IsModer | IsOwner,
    ]


class LessonUpdateAPIView(UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [
        IsAuthenticated,
        IsModer | IsOwner,
    ]

    def perform_update(self, serializer):
        lesson = serializer.save()
        lesson.course.update_last_update()  # при изменении урока нужно обновить дату в курсе
        Notifications.objects.get_or_create(course=lesson.course)


class LessonDeleteAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [
        IsAuthenticated,
        IsOwner | ~IsModer,
    ]


class SubscriptionAPIView(APIView):
    # serializer_class = ...
    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course")
        course = get_object_or_404(Course, pk=course_id)

        try:
            subscription = Subscription.objects.get(user=user, course=course)
            subscription.delete()
            stat = status.HTTP_204_NO_CONTENT
            data = None
        except Subscription.DoesNotExist as e:
            Subscription.objects.create(user=user, course=course)
            stat = status.HTTP_201_CREATED
            data = {"user": user.pk, "course": course.pk}

        return Response(data, status=stat)
