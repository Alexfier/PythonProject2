# -*- coding: utf-8 -*-
import requests
from config.settings import BOT_TOKEN, TELEGRAM_URL
from habit_tracker.models import HabitModel


def send_habit(chat_id, message):
    """Функция для отправки напоминаяния опривычке пользователю"""
    params = {
        "text": message,
        "chat_id": chat_id,
    }
    req = requests.get(f"{TELEGRAM_URL}{BOT_TOKEN}/sendMessage", params=params)
    return req


def message_compose(habit: HabitModel) -> str:
    """Функция формирует сообщение для отправки пользователю.
    Принимает в качестве аргумента объект model: habit_tracker.HabitModel."""
    perform_time = habit.perform_time
    substance = habit.substance
    location = habit.location
    reword = habit.reword
    pleasant_hab = habit.pleasant_hab
    lasting_time = habit.lasting_time

    if reword:
        reword_type = reword
    elif pleasant_hab:
        reword_type = pleasant_hab

    if location:
        message = (
            f"Сегодня в {perform_time} не забудь {substance} в {location} "
            f"течении {lasting_time}. Награди себя {reword_type.name}! :)"
        )
    else:
        message = (
            f"Сегодня в {perform_time} не забудь {substance} "
            f"течении {lasting_time}. Награди себя {reword_type.name}! :)"
        )
    return message
