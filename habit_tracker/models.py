# -*- coding: utf-8 -*-
from django.db import models


class RewordModel(models.Model):
    """Модель вознаграждения model: habit_tracker.models.RewordModel."""

    user = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.CASCADE,
        verbose_name="Автор привички",
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=200, verbose_name="название вознаграждения")
    description = models.CharField(
        max_length=1000, verbose_name="описнаие вознаграждения"
    )

    def __str__(self):
        return f"Вознаграждение {self.name}"

    class Meta:
        verbose_name = "Вознаграждение"
        verbose_name_plural = "Вознаграждения"


class HabitModel(models.Model):
    """Модель привычки model: habit_tracker.models.HabitModel."""

    DAILY = "ежедневно"
    EVERY_TWO_DAYS = "каждые два дня"
    WEEKLY = "еженедельно"

    STATUS_IN_CHOICES = [
        (DAILY, "ежедневно"),
        (EVERY_TWO_DAYS, "каждые два дня"),
        (WEEKLY, "еженедельно"),
    ]

    created_at = models.DateField(
        auto_now_add=True, verbose_name="дата создания привычки"
    )
    name = models.CharField(max_length=200, verbose_name="Название привычки")
    user = models.ForeignKey(
        "users.CustomUser",
        on_delete=models.CASCADE,
        verbose_name="Автор привички",
        related_name="user",
        blank=True,
    )
    location = models.CharField(max_length=400, verbose_name="место выполнеия привычки")
    perform_time = models.TimeField(verbose_name="когда выполнять привичку", null=True)
    substance = models.CharField(max_length=2000, verbose_name="содержание привычки")
    is_pleasant = models.BooleanField(
        verbose_name="признак приятной привычки", default=False
    )
    period = models.CharField(
        max_length=20,
        choices=STATUS_IN_CHOICES,
        default=DAILY,
        verbose_name="периодичность выполнения",
    )
    reword = models.ForeignKey(
        "habit_tracker.RewordModel",
        verbose_name="вознаграждение",
        null=True,
        on_delete=models.SET_NULL,
    )
    pleasant_hab = models.ForeignKey(
        "habit_tracker.HabitModel",
        verbose_name="приятная привычка",
        null=True,
        on_delete=models.SET_NULL,
    )
    lasting_time = models.TimeField(
        verbose_name="длительность выполнения",
    )
    is_public = models.BooleanField(default=False, verbose_name="признак публичности")

    def __str__(self):
        if self.is_pleasant:
            return f"Привычка {self.name}"
        else:
            return f"Привычка {self.name}, выполняется {self.period}."

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
