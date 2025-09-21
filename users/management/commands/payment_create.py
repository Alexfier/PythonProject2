from django.core.management.base import BaseCommand

from courses.models import Course, Lesson
from users.models import CustomsUser, Payments


class Command(BaseCommand):
    """команда для создания платежа"""

    def handle(self, *args, **kwargs):
        user1 = CustomsUser.objects.get(id=1)
        course1 = Course.objects.get(id=1)
        lesson1 = Lesson.objects.get(id=1)

        Payments.objects.create(
            user=user1,
            paid_course=course1,
            paid_lesson=lesson1,
            payment_amount=100.00,
            payment_method="CASH",
        )

        self.stdout.write(self.style.SUCCESS("Платёжная запись успешно создана."))
