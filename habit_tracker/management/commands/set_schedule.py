# -*- coding: UTF-8 -*-
from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, IntervalSchedule


class Command(BaseCommand):
    help = "Create schedule for a task"

    def handle(self, *args, **options):

        IntervalSchedule.objects.all().delete()

        new_schedule = {"every": 600, "period": IntervalSchedule.SECONDS}

        schedule, created = IntervalSchedule.objects.get_or_create(**new_schedule)

        new_task = {
            "interval": schedule,
            "name": "reminder_task",
            "task": "habit_tracker.tasks.reminder_task",
        }

        PeriodicTask.objects.create(**new_task)

        self.stdout.write(
            self.style.SUCCESS("Установленно расписание для задачи user_deactivate")
        )
