import datetime

from rest_framework.serializers import ValidationError

from habit_tracker.models import HabitModel


class ExcludeRewordValidator:
    """Валидатор для исключения одновоеменного
    выбора приятной привычки и вознаграждения"""

    def __init__(self, field_pls, field_rew):
        self.field_pls = field_pls
        self.field_rew = field_rew

    def __call__(self, value):
        field_pls = dict(value).get(self.field_pls, False)
        field_rew = dict(value).get(self.field_rew, False)
        if field_rew and field_pls:
            raise ValidationError(
                detail="Нельзя одновременно выбирать приятную привычку и вознаграждение"
            )


def check_reword(field_pls, field_rew, habit_id):
    """Валидатор проверяет невозможность добавить вознаграждение к приятной привычке
    и одновременно добавить вознаграждение и приятную привычку"""
    if HabitModel.objects.filter(id=habit_id, is_pleasant=True).exists() and (
        field_pls or field_rew
    ):
        raise ValidationError(
            detail="К приятной привычке нельзя привязать другую приятную привычку или вознаграждение"
        )

    elif (
        HabitModel.objects.filter(id=habit_id, pleasant_hab__isnull=False).exists()
        and field_rew
    ):
        raise ValidationError(
            detail="К привычке нельзя привязать вознаграждение, если за нее назначена приятная привычка"
        )

    elif (
        HabitModel.objects.filter(id=habit_id, reword__isnull=False).exists()
        and field_pls
    ):
        raise ValidationError(
            detail="К привычке нельзя привязать приятную привычку, если к за нее назначено вознаграждение"
        )


def is_pleasant_validator(value):
    """Валидатор для провреки связанной model: habit_tracker.HabitModel.
    Параметр модели is_pleasant должен быть True."""
    if HabitModel.objects.filter(id=value, is_pleasant=False).exists():
        raise ValidationError(detail="Привычка не относится к приятным.")


class PeriodValidator:
    """Валидатор для проверки периода выполения привычки.
    Не дожен быть реже раза в неделю"""

    def __init__(self, field_period, field_last_time):
        self.field_period = field_period
        self.field_last_time = field_last_time

    def __call__(self, value):
        period = dict(value).get(self.field_period)
        last_time = dict(value).get(self.field_last_time)

        if last_time and (last_time > datetime.time(minute=2)):
            raise ValidationError(
                detail="Время выполнения не должно быть больше 120 сек."
            )
        if period and (period not in ("ежедневно", "каждые два дня", "еженедельно")):
            raise ValidationError(
                detail="Привычку нельзя выполнять реже 1 раза в неделю."
            )
