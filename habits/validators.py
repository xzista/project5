from rest_framework import serializers


def validate_mutual_exclusion(reward_text, related_habit):
    """
    Нельзя одновременно указывать вознаграждение и связанную привычку.
    """
    if reward_text and related_habit:
        raise serializers.ValidationError(
            "Нельзя одновременно указывать вознаграждение и связанную привычку."
        )


def validate_duration(duration_seconds):
    """
    Время выполнения не должно превышать 120 секунд.
    """
    if duration_seconds and duration_seconds > 120:
        raise serializers.ValidationError(
            "Время выполнения не должно превышать 120 секунд (2 минуты)."
        )


def validate_periodicity(period_days):
    """
    Периодичность выполнения — от 1 до 7 дней.
    """
    if period_days and not (1 <= period_days <= 7):
        raise serializers.ValidationError(
            "Периодичность выполнения должна быть от 1 до 7 дней."
        )


def validate_related_habit(related_habit):
    """
    Связанная привычка должна быть приятной.
    """
    if related_habit and not related_habit.is_pleasant:
        raise serializers.ValidationError(
            "Связанная привычка должна быть помечена как приятная (is_pleasant=True)."
        )


def validate_pleasant_habit(is_pleasant, reward_text, related_habit):
    """
    У приятной привычки не может быть вознаграждения или связанной привычки.
    """
    if is_pleasant and (reward_text or related_habit):
        raise serializers.ValidationError(
            "У приятной привычки не может быть вознаграждения или связанной привычки."
        )