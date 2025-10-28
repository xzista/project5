from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Habit(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='habits'
    )
    place = models.CharField(max_length=255, blank=True)
    time = models.TimeField()
    action = models.CharField(max_length=255)
    is_pleasant = models.BooleanField(default=False)
    related_habit = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL, related_name='linked_by'
    )
    period_days = models.PositiveSmallIntegerField(default=1)
    reward_text = models.CharField(max_length=255, blank=True, null=True)
    duration_seconds = models.PositiveSmallIntegerField(default=60)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ['-created_at']

    def clean(self):
        if self.duration_seconds and self.duration_seconds > 120:
            raise ValidationError({'duration_seconds': 'Время выполнения не должно превышать 120 секунд.'})

        if not (1 <= self.period_days <= 7):
            raise ValidationError({'period_days': 'Периодичность должна быть от 1 до 7 дней.'})

        if self.is_pleasant:
            if self.reward_text:
                raise ValidationError({'reward_text': 'Приятная привычка не может иметь вознаграждение.'})
            if self.related_habit is not None:
                raise ValidationError({'related_habit': 'Приятная привычка не может быть связана с другой привычкой.'})

        if self.reward_text and self.related_habit:
            raise ValidationError('Нельзя указывать одновременно поле вознаграждения и связанную привычку.')

        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError({'related_habit': 'Связанная привычка должна быть помечена как приятная.'})

        if self.related_habit and self.related_habit == self:
            raise ValidationError({'related_habit': 'Привычка не может быть связана сама с собой.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.action} в {self.time} ({'приятная' if self.is_pleasant else 'полезная'})"