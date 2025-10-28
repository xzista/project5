from rest_framework import serializers

from habits.models import Habit
from habits.validators import (validate_duration, validate_mutual_exclusion,
                               validate_periodicity, validate_pleasant_habit,
                               validate_related_habit)


class HabitSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.id")

    class Meta:
        model = Habit
        fields = [
            "id",
            "owner",
            "place",
            "time",
            "action",
            "is_pleasant",
            "related_habit",
            "period_days",
            "reward_text",
            "duration_seconds",
            "is_public",
        ]

    def validate(self, attrs):
        reward_text = attrs.get("reward_text") or getattr(self.instance, "reward_text", None)
        related_habit = attrs.get("related_habit") or getattr(self.instance, "related_habit", None)
        is_pleasant = attrs.get("is_pleasant") or getattr(self.instance, "is_pleasant", False)
        duration_seconds = attrs.get("duration_seconds") or getattr(self.instance, "duration_seconds", None)
        period_days = attrs.get("period_days") or getattr(self.instance, "period_days", None)

        validate_mutual_exclusion(reward_text, related_habit)
        validate_duration(duration_seconds)
        validate_periodicity(period_days)
        validate_related_habit(related_habit)
        validate_pleasant_habit(is_pleasant, reward_text, related_habit)

        return attrs
