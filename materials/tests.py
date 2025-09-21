from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from materials.models import Courses, Lessons
from users.models import User


class LessonsTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email="test-test@test.test", password="12345", is_active=True, is_staff=True, is_superuser=True
        )
        self.client.force_authenticate(user=self.user)

        self.courses = Courses.objects.create(title="Курс", description="Описание курса", owner=self.user)

        self.lessons = Lessons.objects.create(
            title="Урок", description="Описание урока", courses=self.courses, owner=self.user
        )

    def test_lessons_retrieve(self):
        url = reverse("materials:lesson", args=(self.lessons.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lessons.title)

    def test_lessons_list(self):
        url = reverse("materials:lessons")
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("count"), 1)

    def test_lessons_create(self):
        url = reverse("materials:lesson_create")

        data = {"title": "Урок2", "description": "Описание урока"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data.get("title"), "Урок2")

    def test_lessons_update(self):
        url = reverse("materials:lesson_update", args=(self.lessons.pk,))
        data = {"title": "Урок3"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "Урок3")

    def test_lessons_delete(self):
        url = reverse("materials:lesson_destroy", args=(self.lessons.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lessons.objects.all().count(), 0)


class SubscriptionTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email="test-test@test.test", password="12345", is_active=True, is_staff=True, is_superuser=True
        )
        self.client.force_authenticate(user=self.user)

        self.courses = Courses.objects.create(title="Курс", description="Описание курса", owner=self.user)

    def test_create(self):
        url = reverse("materials:subscription")
        # url_del = reverse("materials:subscription", args=(1,))
        data = {"user": self.user.pk, "course": self.courses.pk}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"message": "подписка добавлена"})
        response_del = self.client.post(url, data)

        self.assertEqual(response_del.status_code, status.HTTP_200_OK)
        self.assertEqual(response_del.data, {"message": "подписка удалена"})
