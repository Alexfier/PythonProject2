from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Courses, Lessons


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email почта")
    phone_number = models.CharField(max_length=25, blank=True, null=True, verbose_name="Номер телефона")
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="Город")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True, verbose_name="Аватарка")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payments(models.Model):

    SELECT_PAYMENT_METHOD = [
        ("C", "cash"),
        ("T", "transfer_to_account"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    date_payments = models.DateField(verbose_name="Дата оплаты")
    paid_lesson = models.ForeignKey(
        Lessons, on_delete=models.CASCADE, verbose_name="Оплаченный урок", blank=True, null=True
    )
    paid_course = models.ForeignKey(
        Courses, on_delete=models.CASCADE, verbose_name="Оплаченный курс", blank=True, null=True
    )
    payment_amount = models.PositiveIntegerField(verbose_name="Сумма оплаты")
    payment_method = models.CharField(
        max_length=25, choices=SELECT_PAYMENT_METHOD, default="C", verbose_name="Способ оплаты"
    )

    payment_link = models.URLField(max_length=400, blank=True, null=True, verbose_name="Ссылка на оплату")
