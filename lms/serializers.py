from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from lms.models import Course, Lesson, Subscription
from lms.validators import OnlyYouTubeLinkValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [
            OnlyYouTubeLinkValidator(field="description"),
            OnlyYouTubeLinkValidator(field="video_url"),
        ]


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = SerializerMethodField()
    is_subscribed = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_lessons_count(self, obj):
        """Возвращает количество уроков в курсе"""
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        """Возвращает True, если текущий пользователь подписан на данный курс"""
        return Subscription.is_exist(self.context.get("request").user.pk, obj.pk)

    class Meta:
        model = Course
        fields = (
            "pk",
            "name",
            "preview",
            "description",
            "lessons_count",
            "is_subscribed",
            "lessons",
        )
        validators = [OnlyYouTubeLinkValidator(field="description")]
