from django.contrib.auth.models import AbstractUser
from django.db import models

from courses.models import Course, Lesson


class CustomsUser(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True,
        verbose_name="Email",
        help_text="Укажите почту",
    )
    phone = models.CharField(
        max_length=35,
        verbose_name="телефон",
        blank=True,
        null=True,
        help_text="введи номер телефона",
    )
    first_name = models.CharField(
        max_length=50,
        verbose_name="Имя",
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name="Фамилия",
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        blank=True,
        null=True,
        verbose_name="Аватар",
    )
    city = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Город",
        help_text="Укажите город",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payments(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ("CASH", "Наличные"),
        ("TRANSFER", "Перевод на счёт"),
    ]
    user = models.ForeignKey(
        CustomsUser,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="пользователь",
    )
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата оплаты")
    paid_course = models.ForeignKey(
        Course,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    payment_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Сумма оплаты",
    )
    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_METHOD_CHOICES,
        verbose_name="Способ оплаты",
    )

    session_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="ID сессии",
        help_text="Укажите ID сессии",
    )

    link = models.URLField(
        max_length=400,
        null=True,
        blank=True,
        verbose_name="Ссылка на оплату",
        help_text="Укажите ссылку на оплату",
    )

    def __str__(self):
        return f"Платёж от {self.user} за {self.paid_course if self.paid_course else self.paid_lesson}"

    class Meta:
        verbose_name = "Платёж"
        verbose_name_plural = "Платежи"
