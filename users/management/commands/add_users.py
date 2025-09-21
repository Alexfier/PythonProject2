# -*- coding: UTF-8 -*-
from django.core.management.base import BaseCommand
from users.models import CustomUser
from habit_tracker.models import HabitModel, RewordModel


class Command(BaseCommand):
    help = "Add users and payments"

    def handle(self, *args, **kwargs):
        CustomUser.objects.all().delete()
        HabitModel.objects.all().delete()
        RewordModel.objects.all().delete()

        users = [
            {
                "email": "user_1@mail.com",
                "username": "User_1",
                "password": "pbkdf2_sha256$870000$cXDyxcfpSsVnOEgcjD0hd9$e8pQZzj6Q5G5P9MYSjAhJ7He5FEOxhktOcasUGtOxAQ=",
                "country": "Russia",
            },
            {
                "email": "user_2@mail.com",
                "username": "User_2",
                "password": "pbkdf2_sha256$870000$k9lZWga6YEePGlyyoZZp0u$dACFQOuJB1EzKRCTvNwnMkr105fVqJ2vUYzsSv9WldQ=",
                "country": "Russia",
            },
        ]

        for user_data in users:
            user, created = CustomUser.objects.get_or_create(**user_data)

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Добавлен пользователь {user.username}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Пользователь уже существует {user.username}")
                )

        pleasant_habits = [
            {
                "name": "pleasant habit #1",
                "user": CustomUser.objects.get(email="user_1@mail.com"),
                "location": "everywhere",
                "lasting_time": "00:02:00",
                "substance": "substance of pleasant habit #1",
                "is_pleasant": True,
            },
            {
                "name": "pleasant habit #2",
                "user": CustomUser.objects.get(email="user_2@mail.com"),
                "location": "everywhere",
                "lasting_time": "00:02:00",
                "substance": "substance of pleasant habit #1",
                "is_pleasant": True,
            },
        ]

        for habit_data in pleasant_habits:
            habit, created = HabitModel.objects.get_or_create(**habit_data)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Создана приятная привычка {habit.name}")
                )
            else:
                self.stdout.write(self.style.WARNING("Привычка уже сужествует"))

        rewords = [
            {
                "user": CustomUser.objects.get(email="user_1@mail.com"),
                "name": "reword #1",
            },
            {
                "user": CustomUser.objects.get(email="user_2@mail.com"),
                "name": "reword #2",
            },
        ]

        for reword_data in rewords:
            reword, created = RewordModel.objects.get_or_create(**reword_data)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Создано вознаграждение {reword.name}")
                )
            else:
                self.stdout.write(self.style.WARNING("Вознаграждение уже сужествует"))

        good_habits = [
            {
                "name": "good habit #1",
                "user": CustomUser.objects.get(email="user_1@mail.com"),
                "location": "everywhere",
                "perform_time": "10:00:00",
                "lasting_time": "00:02:00",
                "period": "ежедневно",
                "substance": "substance of good habit #1",
                "reword": RewordModel.objects.get(name="reword #1"),
                "is_public": True,
            },
            {
                "name": "good habit #2",
                "user": CustomUser.objects.get(email="user_1@mail.com"),
                "location": "everywhere",
                "perform_time": "08:00:00",
                "lasting_time": "00:02:00",
                "period": "еженедельно",
                "substance": "substance of good habit #2",
                "pleasant_hab": HabitModel.objects.get(name="pleasant habit #1"),
            },
            {
                "name": "good habit #3",
                "user": CustomUser.objects.get(email="user_2@mail.com"),
                "location": "everywhere",
                "perform_time": "12:00:00",
                "lasting_time": "00:02:00",
                "period": "каждые два дня",
                "substance": "substance of good habit #3",
                "reword": RewordModel.objects.get(name="reword #2"),
            },
            {
                "name": "good habit #4",
                "user": CustomUser.objects.get(email="user_1@mail.com"),
                "location": "everywhere",
                "perform_time": "20:00:00",
                "lasting_time": "00:10:00",
                "substance": "substance of good habit #4",
                "period": "каждые два дня",
                "pleasant_hab": HabitModel.objects.get(name="pleasant habit #2"),
                "is_public": True,
            },
        ]

        for habit_data in good_habits:
            habit, created = HabitModel.objects.get_or_create(**habit_data)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Создана хорошая привычка {habit.name}")
                )
            else:
                self.stdout.write(self.style.WARNING("Привычка уже сужествует"))
