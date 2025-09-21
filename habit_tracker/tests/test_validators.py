# -*- coding: UTF-8 -*-
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase
from habit_tracker.models import HabitModel, RewordModel
from users.models import CustomUser


class ValidatorsTestCase(APITestCase):
    """Тестирование валидаторов habit_traker.validators."""

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

    def test_reword_or_habit(self):
        """Тестирование валидации при одновремееном указании приятной привычки и вознаграждения"""

        data = {
            "name": "good habit in valid",
            "location": "everywhere",
            "perform_time": "08:00:00",
            "lasting_time": "00:02:00",
            "substance": "substance of good habit #1",
            "period": "ежедневно",
            "reword": self.reword_1.pk,
            "pleasant_hab": self.pleasant_habit_1.pk,
        }

        request = self.client.post("/habits/", data=data)
        self.assertRaises(ValidationError)
        self.assertEqual(
            request.json().get("non_field_errors"),
            ["Нельзя одновременно выбирать приятную привычку и вознаграждение"],
        )

    def test_lasting_time(self):
        """Тестирование валидации времени выполнения меннее 120 сек."""

        data = {
            "name": "good habit in valid",
            "location": "everywhere",
            "perform_time": "08:00:00",
            "lasting_time": "00:20:00",
            "substance": "substance of good habit #1",
            "period": "ежедневно",
            "reword": self.reword_1.pk,
        }

        request = self.client.post("/habits/", data=data)
        self.assertRaises(ValidationError)
        self.assertEqual(
            request.json().get("non_field_errors"),
            ["Время выполнения не должно быть больше 120 сек."],
        )

    def test_period_habit(self):
        """Тестирование валидации пероида выполнения привычки"""
        data = {
            "name": "good habit in valid",
            "location": "everywhere",
            "perform_time": "08:00:00",
            "lasting_time": "00:20:00",
            "substance": "substance of good habit #1",
            "period": "каждые 2 недели",
            "reword": self.reword_1.pk,
        }

        request = self.client.post("/habits/", data=data)
        self.assertEqual(
            request.json().get("period"), ['"каждые 2 недели" is not a valid choice.']
        )
        self.assertRaises(ValidationError)
