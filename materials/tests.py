from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import User


class LessonsTest(APITestCase):
    """ Тесты для модели Уроки """

    def setUp(self):
        """Задает начальные данные для тестов."""
        self.user = User.objects.create_user(email="test@gmail.com", password="password", )
        self.user.is_staff = True  # Убедитесь, что пользователь сделан администратором
        self.user.is_active = True  # Пользователь активен
        self.user.save()  # Не забывайте сохранять изменения

        # Авторизация
        self.client.force_authenticate(user=self.user)
        # Создание урока
        self.lesson = Lesson.objects.create(title='Test 1', link_to_the_video="https://www.youtube.com/lesson1/",
                                            owner=self.user)

    def test_lesson_retrieve(self):
        """ Проверяем GET-запрос """
        url = reverse("materials:lesson-get", args=(self.lesson.id,))
        response = self.client.get(url)
        data = response.json()

        # None != 10
        self.assertEqual(data.get("owner"), self.user.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)

    def test_lesson_list(self):
        """ Проверяем вывод списка объектов """
        url = reverse("materials:lesson-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_post(self):
        """ Проверяем POST-запрос """
        url = reverse("materials:lesson-create")
        data = {
            'title': 'Test 2',
            'owner': self.user.pk,
        }
        response = self.client.post(url, data=data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Lesson.objects.all().exists())


    def test_lesson_delete(self):
        """Тест удаления урока по Primary Key."""
        url = reverse("materials:lesson-delete", args=(self.lesson.id,))
        response = self.client.delete(url)

        # 6 != 1
        self.assertEqual(self.lesson.id, 1)
        self.assertEqual(Lesson.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class CourseTest(APITestCase):
    """ Тесты для модели Курсы """

    def setUp(self):
        """Задает начальные данные для тестов."""
        self.user = User.objects.create_user(email="test@gmail.com", password="password", )
        self.user.is_staff = True  # Убедитесь, что пользователя сделать администратором
        self.user.is_active = True  # Пользователь активен
        self.user.save()  # Не забывайте сохранять изменения

        # Авторизация
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title='Курс', description="Описание",
                                            owner=self.user)

    def test_course_retrieve(self):
        """ Проверяем GET-запрос """
        url = reverse("materials:course-detail", args=(self.course.id,))

        response = self.client.get(url)
        data = response.json()

        self.assertEqual(data.get("owner"), self.user.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_course_list(self):
        url = reverse("materials:course-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_course_post(self):
        """ Проверяем POST-запрос """
        url = reverse("materials:course-list")
        data = {
            'title': 'Курс 2',
            'owner': self.user.pk,
            'description': 'Описание 2'
        }
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Course.objects.all().exists())

    # def test_course_put(self):
    #     url = reverse("materials:course-detail", args=(self.course.id,))
    #     data = {
    #         'title': '1 Курс',
    #         'description': '1 Описание'
    #     }
    #     response = self.client.put(url, data=data)
    #     print('test_lesson_put', response.data)
    #
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_course_delete(self):
        url = reverse("materials:course-detail", args=(self.course.id,))
        response = self.client.delete(url)

        self.assertEqual(self.course.id, 1)
        self.assertEqual(Course.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class SubscriptionTest(APITestCase):
    """ Тесты для модели Подписки """

    def setUp(self):
        """Задает начальные данные для тестов."""
        self.user = User.objects.create_user(email="test@gmail.com", password="password", )
        self.user.is_staff = True  # Убедитесь, что пользователя сделать администратором
        self.user.is_active = True  # Пользователь активен
        self.user.save()  # Не забывайте сохранять изменения

        # Авторизация
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(title='Курс', description="Описание",
                                            owner=self.user)
        self.subscription = Subscription.objects.create(course=self.course, user=self.user)


    def test_subscription_retrieve(self):
        url = reverse("materials:subscription-detail", args=[self.subscription.id])

        response = self.client.get(url)
        data = response.json()
        print('test_subscription_retrieve', data)

        self.assertEqual(data.get("user"), self.user.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_subscription_list(self):
        url = reverse("materials:subscription-list")
        response = self.client.get(url)
        print('test_course_list', response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_subscription_post(self):
        url = reverse("materials:subscription-list")
        data = {
            "course": self.course.id,
            "user": self.user.id
        }
        response = self.client.post(url, data=data)
        print('test_lesson_post', response.data)

        # 400 != 201
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Subscription.objects.all().exists())


    def test_subscription_put(self):
        url = reverse("materials:subscription-detail", args=(self.subscription.id,))
        data = {
            'curse': 2
            # 'user': self.user
        }
        response = self.client.put(url, data=data)
        print('test_lesson_put', response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_subscription_delete(self):
        url = reverse("materials:subscription-detail", args=(self.subscription.id,))
        response = self.client.delete(url)

        # 11 != 1
        self.assertEqual(self.subscription.id, 1)
        self.assertEqual(Subscription.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
