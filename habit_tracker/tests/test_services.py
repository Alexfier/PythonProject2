# -*- coding: UTF-8 -*-
from unittest.mock import patch
from rest_framework.test import APITestCase
from config.settings import TELEGRAM_URL, BOT_TOKEN
from habit_tracker.models import HabitModel, RewordModel
from habit_tracker.services import message_compose, send_habit
from users.models import CustomUser
from rest_framework.response import Response


class ServicesTestCase(APITestCase):

    def __init__(self, *args, **kwargs):
        self.maxDiff = None
        super().__init__(*args, **kwargs)

    def setUp(self):
        user_data = {
            "chat_id": "12345",
            "username": "test_user_1",
            "email": "test_user_1@mail.com",
            "password": "12345",
        }

        self.test_user_1 = CustomUser.objects.create_user(**user_data)

        pleasant_habit = {
            "name": "pleasant habit #1",
            "user": self.test_user_1,
            "location": "everywhere",
            "lasting_time": "00:10:00",
            "substance": "substance of pleasant habit #1",
        }

        self.pleasant_habit_1 = HabitModel.objects.create(**pleasant_habit)

        reword = {"user": self.test_user_1, "name": "test reword #1"}

        self.reword_1 = RewordModel.objects.create(**reword)

        good_habits = {
            "name": "good habit #1",
            "user": self.test_user_1,
            "location": "everywhere",
            "perform_time": "08:00:00",
            "lasting_time": "00:10:00",
            "substance": "substance of good habit #1",
            "period": "ежедневно",
            "reword": self.reword_1,
            "is_public": True,
        }

        self.good_habit_1 = HabitModel.objects.create(**good_habits)

    @patch("requests.get")
    def test_send_habit(self, mock_get):
        """Тестирование формирования сообщения и отправки его в чат Telegram."""
        mock_response = Response()
        mock_response.status_code = 200
        mock_response._content = '{"ok": true, "result": {}}'
        mock_get.return_value = mock_response

        chat_id = self.test_user_1.chat_id
        message = message_compose(self.good_habit_1)

        response = send_habit(chat_id, message)

        mock_get.assert_called_once_with(
            f"{TELEGRAM_URL}{BOT_TOKEN}/sendMessage",
            params={"text": message, "chat_id": chat_id},
        )
        self.assertEqual(response.status_code, 200)
