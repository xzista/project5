import json
import os

from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import requests


User = get_user_model()

def send_message(chat_id, text):
    """Отправка сообщения через Telegram Bot API"""
    url = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_TOKEN')}/sendMessage"
    requests.post(url, data={"chat_id": chat_id, "text": text})


@csrf_exempt
def telegram_webhook(request):
    """Обработка сообщений от Telegram"""
    data = json.loads(request.body.decode("utf-8"))
    message = data.get("message", {})
    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "").strip()

    if text == "/start":
        send_message(chat_id, "👋 Привет! Напиши свой email, который ты использовал при регистрации.")
        return JsonResponse({"ok": True})

    try:
        user = User.objects.get(email=text)
        user.tg_chat_id = chat_id
        user.save()
        send_message(chat_id, f"Отлично, {user.username}! Теперь я буду присылать напоминания о привычках.")
    except User.DoesNotExist:
        send_message(chat_id, "Пользователь с таким email не найден. Попробуй снова.")

    return JsonResponse({"ok": True})