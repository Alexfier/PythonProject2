from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Courses, Lessons, Subscription
from .validators import CorrectUrl


class LessonsModelSerializer(ModelSerializer):

    class Meta:
        model = Lessons
        fields = "__all__"
        validators = [CorrectUrl(field="link")]


class CoursesModelSerializer(ModelSerializer):
    count_lessons = SerializerMethodField()
    lessons = LessonsModelSerializer(many=True, read_only=True)
    subscription = SerializerMethodField()

    def get_count_lessons(self, courses):
        return Lessons.objects.filter(courses=courses).count()

    def get_subscription(self, key):
        return Subscription.objects.filter(course=key).exists()

    class Meta:
        model = Courses
        fields = "__all__"
        validators = [CorrectUrl(field="link")]
