from django.db import models

from config.settings import AUTH_USER_MODEL


class Courses(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название курса")
    image = models.ImageField(upload_to="preview/", blank=True, null=True, verbose_name="Предварительный просмотр")
    description = models.TextField(blank=True, null=True, verbose_name="Описание курса")
    owner = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Создатель курса"
    )
    link = models.CharField(max_length=10000, blank=True, null=True, verbose_name="Ссылка на видео")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lessons(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название урока")
    image = models.ImageField(
        upload_to="preview/lessons/", blank=True, null=True, verbose_name="Предварительный просмотр"
    )
    description = models.TextField(blank=True, null=True, verbose_name="Описание урока")
    link = models.CharField(max_length=10000, blank=True, null=True, verbose_name="Ссылка на видео")
    courses = models.ForeignKey(
        Courses, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Курс", related_name="lessons"
    )
    owner = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Создатель урока"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Subscription(models.Model):
    user = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Пользователь"
    )
    course = models.ForeignKey(
        Courses, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Курс", related_name="courses"
    )
    subscription = models.BooleanField(default=False, verbose_name="Подписка")

    def __str__(self):
        return "Статус активной подписки"

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
