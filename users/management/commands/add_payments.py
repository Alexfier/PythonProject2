from django.core.management.base import BaseCommand
from users.models import Payment
from materials.models import Course, Lesson
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Add data to database"

    def handle(self, *args, **options):
        User.objects.all().delete()
        Lesson.objects.all().delete()
        Course.objects.all().delete()
        Payment.objects.all().delete()

        user1 = User.objects.create(
            email="student1@example.com",
        )

        user2 = User.objects.create(
            email="student2@example.com",
        )

        # Создаем тестовые курсы
        course1 = Course.objects.create(
            name="Python-разработчик",
            description="Полный курс по Python и Django",
        )

        course2 = Course.objects.create(
            name="Веб-разработка",
            description="Курс по созданию веб-приложений",
        )

        # Создаем тестовые уроки
        # lesson1 = Lesson.objects.create(
        #     name="Основы Python",
        #     description="Введение в язык Python",
        #     video_link="https://example.com/python-basics",
        #     course=course1,
        # )

        lesson2 = Lesson.objects.create(
            name="Django ORM",
            description="Работа с моделями в Django",
            video_link="https://example.com/django-orm",
            course=course1,
        )

        lesson3 = Lesson.objects.create(
            name="HTML и CSS",
            description="Основы верстки",
            video_link="https://example.com/html-css",
            course=course2,
        )

        # Создаем тестовые платежи
        payment_data = [
            {
                "user": user1,
                "paid_course": course1,
                "paid_lesson": None,
                "amount": 15000,
                "payment_method": "transfer",
                "payment_date": "2025-03-03",
            },
            {
                "user": user1,
                "paid_course": None,
                "paid_lesson": lesson2,
                "amount": 2000,
                "payment_method": "cash",
                "payment_date": "2025-04-03",
            },
            {
                "user": user2,
                "paid_course": course2,
                "paid_lesson": None,
                "amount": 12000,
                "payment_method": "transfer",
                "payment_date": "2025-04-04",
            },
            {
                "user": user2,
                "paid_course": None,
                "paid_lesson": lesson3,
                "amount": 1500,
                "payment_method": "cash",
                "payment_date": "2025-05-06",
            },
        ]

        for data in payment_data:
            Payment.objects.create(**data)

        self.stdout.write(self.style.SUCCESS("Тестовые данные успешно созданы!"))
