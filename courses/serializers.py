from rest_framework.serializers import ModelSerializer, SerializerMethodField

from courses.models import Course, Lesson, Subscription
from courses.validators import LinkToVideoValidator


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [LinkToVideoValidator(field="link_to_video")]


class CourseSerializer(ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    lesson_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_lesson_count(self, course):
        return Lesson.objects.filter(course=course).count()

    class Meta:
        model = Course
        fields = ("title", "description", "lessons", "lesson_count")


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"

        def get_is_subscribed(self, obj):
            user = self.context["request"].user
            return Subscription.objects.filter(user=user, course=obj).exists()
