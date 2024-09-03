from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from lms.models import Course, Lesson
from lms.validators import OnlyYouTubeLinkValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [OnlyYouTubeLinkValidator(field='description'), OnlyYouTubeLinkValidator(field='video_url')]


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Course
        fields = ("pk", "name", "preview", "description", "lessons_count", "lessons")
        validators = [OnlyYouTubeLinkValidator(field='description')]
