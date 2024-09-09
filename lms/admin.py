from django.contrib import admin

from lms.models import Course, Lesson, Subscription, Notifications


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'preview', 'description', 'owner')
    readonly_fields = ('last_update',)
    list_filter = ('name', 'owner')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'description', 'preview', 'video_url', 'owner')
    list_filter = ('name', 'owner')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'course')
    list_filter = ('user', 'course')


@admin.register(Notifications)
class NotificationsAdmin(admin.ModelAdmin):
    list_display = ('course',)
    list_filter = ('course',)
