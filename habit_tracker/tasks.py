# -*- coding: utf-8 -*-
from datetime import timedelta
from django.utils import timezone
from habit_tracker.models import HabitModel
from habit_tracker.services import message_compose, send_habit
from celery import shared_task


@shared_task
def reminder_task():
    """Отложенная задача для получения экземпляров model: habit_tracker.HabitModel
    у которых время выполения отстоит на 10 минут от текущего"""

    delta = timezone.now() + timedelta(minutes=10)

    queryset = HabitModel.objects.filter(perform_time__range=(timezone.now(), delta))
    print(queryset)
    for object in queryset:
        if object.period == "ежедневно":
            chat_id = object.user.chat_id
            print(chat_id, object.period)
            message = message_compose(object)
            send_habit(chat_id=chat_id, message=message)

        if object.period == "каждые два дня":
            time_dif = timezone.now() - object.created_at
            if time_dif.day % 2 == 0:
                message = message_compose(object)
                send_habit(chat_id=chat_id, message=message)

        if object.period == "еженедельно":
            time_dif = timezone.now() - object.created_at
            if time_dif.day % 7 == 0:
                message = message_compose(object)
                send_habit(chat_id=chat_id, message=message)


@shared_task
def control_task():
    return "celary is working!"
