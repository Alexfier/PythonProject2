from django.db import models

from config.settings import AUTH_USER_MODEL


class Course(models.Model):
    """Модель курса."""

    title = models.CharField(
        max_length=150,
        verbose_name="Название курса",
    )
    description = models.TextField(
        max_length=250,
        blank=True,
        null=True,
        verbose_name="Описание курса",
    )
    preview = models.ImageField(
        upload_to="courses/img_course/",
        verbose_name="превью",
        blank=True,
        null=True,
    )
    owner = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Владелец",
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Модель урока."""

    title = models.CharField(
        max_length=150,
        verbose_name="Название урока",
    )
    description = models.TextField(
        max_length=250,
        blank=True,
        null=True,
        verbose_name="Описание урока",
    )
    preview = models.ImageField(
        upload_to="courses/img_lesson/",
        verbose_name="превью",
        blank=True,
        null=True,
    )
    link_to_video = models.URLField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Ссылка на видео",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс",
        related_name="lessons",
    )
    owner = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Владелец",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Subscription(models.Model):
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="Пользователь",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="Курс",
    )

    def __str__(self):
        return {self.user} - {self.course}

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
