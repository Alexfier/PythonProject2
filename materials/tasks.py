import datetime
from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail

from config.settings import DEFAULT_FROM_EMAIL
from users.models import User

from .models import Subscription


@shared_task
def send_mail_after_course_update():
    subscriptions = Subscription.objects.all()
    subscriptions_list = []
    for subscription in subscriptions:
        subscriptions_list.append(subscription.user.email)
    send_mail(
        "Вышел новый урок", "По курсу из Вашей подписки появился новый урок!", DEFAULT_FROM_EMAIL, subscriptions_list
    )


@shared_task
def blocking_user():
    users = User.objects.all()
    timeout = datetime.datetime.today().date() - timedelta(days=30)
    for user in users:
        if user.last_login < timeout:
            user.is_active = False


if __name__ == "__main__":
    blocking_user()
