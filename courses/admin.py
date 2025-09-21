from django.contrib import admin

from courses.models import Course, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "preview")
    search_fields = ("name",)
    search_filter = ("name",)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "preview", "link_to_video")
    search_fields = ("name",)
    search_filter = ("name",)
