import os

import requests
from datetime import datetime
from celery import shared_task
from django.conf import settings
from habits.models import Habit

TELEGRAM_API_URL = os.getenv('TELEGRAM_URL')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_TOKEN')


@shared_task
def send_habit_reminders():
    """
    Проверка привычек,
    время которых совпадает с текущим часом/минутой,
    и отправление уведомления в Telegram.
    """
    now = datetime.now().time().replace(second=0, microsecond=0)
    habits = Habit.objects.filter(time__hour=now.hour, time__minute=now.minute)

    for habit in habits:
        if not habit.owner.profile.telegram_chat_id:
            continue

        message = f"⏰ Напоминание!\nСегодня пора выполнить привычку:\n👉 {habit.action} в {habit.place}"
        send_telegram_message(habit.owner.profile.telegram_chat_id, message)


def send_telegram_message(chat_id, text):
    """Отправка сообщения через Telegram Bot API"""
    url = TELEGRAM_API_URL.format(token=settings.TELEGRAM_BOT_TOKEN)
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, data=payload)