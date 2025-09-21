# -*- coding: UTF-8 -*-
from rest_framework import status
from rest_framework.test import APITestCase
from habit_tracker.models import HabitModel, RewordModel
from users.models import CustomUser


class HabitCRUDTestCase(APITestCase):
    """Тестирование CRUD операций над model:habit_tracker.HabitModel."""

    def setUp(self):
        user_data = [
            {
                "username": "test_user_1",
                "email": "test_user_1@mail.com",
                "password": "12345",
            },
            {
                "username": "test_user_2",
                "email": "test_user_2@mail.com",
                "password": "12345",
            },
        ]

        self.test_user_1 = CustomUser.objects.create_user(**user_data[0])

        self.test_user_2 = CustomUser.objects.create_user(**user_data[1])

        pleasant_habit = [
            {
                "name": "pleasant habit #1",
                "user": self.test_user_1,
                "location": "everywhere",
                "lasting_time": "00:10:00",
                "substance": "substance of pleasant habit #1",
            },
            {
                "name": "pleasant habit #2",
                "user": self.test_user_2,
                "location": "everywhere",
                "lasting_time": "00:10:00",
                "substance": "substance of pleasant habit #1",
            },
        ]

        self.pleasant_habit_1 = HabitModel.objects.create(**pleasant_habit[0])
        self.pleasant_habit_2 = HabitModel.objects.create(**pleasant_habit[1])

        reword = {"user": self.test_user_1, "name": "test reword #1"}

        self.reword_1 = RewordModel.objects.create(**reword)

        good_habits = [
            {
                "name": "good habit #1",
                "user": self.test_user_1,
                "location": "everywhere",
                "perform_time": "08:00:00",
                "lasting_time": "00:10:00",
                "substance": "substance of good habit #1",
                "period": "ежедневно",
                "reword": self.reword_1,
                "is_public": True,
            },
            {
                "name": "good habit #2",
                "user": self.test_user_1,
                "location": "everywhere",
                "perform_time": "12:00:00",
                "lasting_time": "00:10:00",
                "substance": "substance of good habit #1",
                "period": "каждые два дня",
                "pleasant_hab": self.pleasant_habit_1,
            },
            {
                "name": "good habit #3",
                "user": self.test_user_2,
                "location": "everywhere",
                "perform_time": "08:00:00",
                "lasting_time": "00:10:00",
                "substance": "substance of good habit #3",
                "period": "ежедневно",
                "reword": self.reword_1,
                "is_public": True,
            },
            {
                "name": "good habit #4",
                "user": self.test_user_2,
                "location": "everywhere",
                "perform_time": "12:00:00",
                "lasting_time": "00:10:00",
                "substance": "substance of good habit #4",
                "period": "каждые два дня",
                "pleasant_hab": self.pleasant_habit_2,
            },
        ]

        self.good_habit_1 = HabitModel.objects.create(**good_habits[0])
        self.good_habit_2 = HabitModel.objects.create(**good_habits[1])
        self.good_habit_3 = HabitModel.objects.create(**good_habits[2])
        self.good_habit_4 = HabitModel.objects.create(**good_habits[3])

        self.client.force_authenticate(user=self.test_user_1)

    def test_get_habit(self):
        """Тестиирование получения объекта model:habit_tracker.HabitModel."""

        request = self.client.get(f"/habits/{self.good_habit_1.pk}/")

        self.assertEqual(request.status_code, status.HTTP_200_OK)

        self.assertEqual(
            request.json(),
            {
                "is_pleasant": False,
                "is_public": True,
                "lasting_time": "00:10:00",
                "location": "everywhere",
                "name": "good habit #1",
                "perform_time": "08:00:00",
                "period": "ежедневно",
                "pleasant_hab": None,
                "reword": self.reword_1.pk,
                "substance": "substance of good habit #1",
                "user": self.test_user_1.pk,
            },
        )

    def test_get_list_habit(self):
        """Тестирование получения списка объектов model:habit_model.HabitModel."""

        request = self.client.get("/habits/")

        self.assertEqual(request.status_code, status.HTTP_200_OK)

        self.assertEqual(
            request.json(),
            {
                "count": 4,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "is_pleasant": False,
                        "is_public": False,
                        "lasting_time": "00:10:00",
                        "location": "everywhere",
                        "name": "pleasant habit #1",
                        "perform_time": None,
                        "period": "ежедневно",
                        "pleasant_hab": None,
                        "reword": None,
                        "substance": "substance of pleasant habit #1",
                        "user": self.test_user_1.pk,
                    },
                    {
                        "is_pleasant": False,
                        "is_public": True,
                        "lasting_time": "00:10:00",
                        "location": "everywhere",
                        "name": "good habit #1",
                        "perform_time": "08:00:00",
                        "period": "ежедневно",
                        "pleasant_hab": None,
                        "reword": self.reword_1.pk,
                        "substance": "substance of good habit #1",
                        "user": self.test_user_1.pk,
                    },
                    {
                        "is_pleasant": False,
                        "is_public": False,
                        "lasting_time": "00:10:00",
                        "location": "everywhere",
                        "name": "good habit #2",
                        "perform_time": "12:00:00",
                        "period": "каждые два дня",
                        "pleasant_hab": self.pleasant_habit_1.pk,
                        "reword": None,
                        "substance": "substance of good habit #1",
                        "user": self.test_user_1.pk,
                    },
                    {
                        "is_pleasant": False,
                        "is_public": True,
                        "lasting_time": "00:10:00",
                        "location": "everywhere",
                        "name": "good habit #3",
                        "perform_time": "08:00:00",
                        "period": "ежедневно",
                        "pleasant_hab": None,
                        "reword": self.reword_1.pk,
                        "substance": "substance of good habit #3",
                        "user": self.test_user_2.pk,
                    },
                ],
            },
        )

    def test_get_public_habit(self):
        """Тестирование получения списка объектов model:habit_tracker.HabitModel у которых параметр is_public=True."""

        request = self.client.get("/habits/public/")

        self.assertEqual(request.status_code, status.HTTP_200_OK)

        self.assertEqual(
            request.json(),
            {
                "count": 2,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "is_pleasant": False,
                        "is_public": True,
                        "lasting_time": "00:10:00",
                        "location": "everywhere",
                        "name": "good habit #1",
                        "perform_time": "08:00:00",
                        "period": "ежедневно",
                        "pleasant_hab": None,
                        "reword": self.reword_1.pk,
                        "substance": "substance of good habit #1",
                        "user": self.test_user_1.pk,
                    },
                    {
                        "is_pleasant": False,
                        "is_public": True,
                        "lasting_time": "00:10:00",
                        "location": "everywhere",
                        "name": "good habit #3",
                        "perform_time": "08:00:00",
                        "period": "ежедневно",
                        "pleasant_hab": None,
                        "reword": self.reword_1.pk,
                        "substance": "substance of good habit #3",
                        "user": self.test_user_2.pk,
                    },
                ],
            },
        )

    def test_create_habit(self):
        """Тестирование создания объекта model:habit_tracker.HabitModel."""

        data = {
            "name": "new pleasant habit",
            "location": "everywhere",
            "lasting_time": "00:02:00",
            "substance": "substance of new pleasant habit",
        }

        request = self.client.post("/habits/", data=data)

        self.assertEqual(request.status_code, status.HTTP_201_CREATED)

    def test_patch_habit(self):
        """Тестирование изменения объекта model:habit_tracker.HabitModel."""

        data = {
            "name": "changed pleasant habit",
        }

        request = self.client.patch(f"/habits/{self.good_habit_1.pk}/", data=data)

        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_delete_habit(self):
        """Тестирование удаления объекта model:habit_tracker.HabitModel."""

        request = self.client.delete(f"/habits/{self.good_habit_1.pk}/")

        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_list_reword(self):
        """Тестирование получения списка объектов model:habit_tracker.RewordModel."""

        request = self.client.get("/rewords/")

        self.assertEqual(request.status_code, status.HTTP_200_OK)

        self.assertEqual(
            request.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "description": "",
                        "id": self.reword_1.pk,
                        "name": "test reword #1",
                        "user": self.test_user_1.pk,
                    }
                ],
            },
        )

    def test_get_reword(self):
        """Тестирование получения объекта model:habit_tracker.RewordModel."""

        request = self.client.get(f"/rewords/{self.reword_1.pk}/")

        self.assertEqual(request.status_code, status.HTTP_200_OK)

        self.assertEqual(
            request.json(),
            {
                "id": self.reword_1.pk,
                "name": "test reword #1",
                "description": "",
                "user": self.test_user_1.pk,
            },
        )

    def test_patch_reword(self):
        """Тестирование изменения объекта model:habit_tracker.RewordModel."""

        data = {
            "name": "changed reword",
        }

        request = self.client.patch(f"/rewords/{self.reword_1.pk}/", data=data)

        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_delete_reword(self):
        """Тестирование удаления объекта model:habit_tracker.RewordModel."""

        request = self.client.delete(f"/rewords/{self.reword_1.pk}/")

        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)
