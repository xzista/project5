# Habit Tracker - Система управления привычками

![Django](https://img.shields.io/badge/Django-4.2-green)
![DRF](https://img.shields.io/badge/DRF-3.14-blue)
![Celery](https://img.shields.io/badge/Celery-5.3-darkgreen)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-teal)
![Docker](https://img.shields.io/badge/Docker-24.0-lightblue)

Веб-сервис для создания, отслеживания и управления привычками с автоматическими напоминаниями через Telegram. Система помогает пользователям формировать полезные привычки и соблюдать их регулярность.

## 📋 Содержание

- [Основные возможности](#-основные-возможности)
- [Архитектура и технологии](#-архитектура-и-технологии)
- [Модели данных](#-модели-данных)
- [Установка и запуск](#-установка-и-запуск)
  - [Локальная установка](#локальная-установка)
  - [Docker-развертывание](#docker-развертывание)
  - [Настройка переменных окружения](#настройка-переменных-окружения)
- [API Endpoints](#-api-endpoints)
- [Интеграция с Telegram](#-интеграция-с-telegram)
- [Валидация данных](#-валидация-данных)
- [Тестирование](#-тестирование)
- [Деплоймент](#-деплоймент)

## ✨ Основные возможности

- **📊 Управление привычками**: Создание полезных и приятных привычек с настраиваемыми параметрами
- **⏰ Автоматические напоминания**: Интеграция с Telegram для отправки уведомлений о времени выполнения привычек
- **🔐 Безопасность**: JWT-аутентификация, права доступа на уровне пользователя
- **🌐 Публичный доступ**: Возможность делиться своими привычками с сообществом
- **📱 RESTful API**: Полностью документированный API для интеграции с фронтендом
- **📈 Пагинация и фильтрация**: Удобный просмотр больших списков привычек
- **⚙️ Валидация**: Проверка бизнес-правил при создании и редактировании привычек

## 🏗️ Архитектура и технологии

### Backend Stack
- **Python 3.11+** - Основной язык программирования
- **Django 4.2+** - Веб-фреймворк
- **Django REST Framework 3.14+** - REST API
- **PostgreSQL 15+** - База данных
- **Celery 5.3+** - Асинхронные задачи
- **Redis 7.0+** - Брокер сообщений и кэш
- **Django CORS Headers** - Поддержка CORS
- **drf-yasg** - Документация Swagger

### DevOps
- **Docker & Docker Compose** - Контейнеризация
- **Poetry** - Управление зависимостями
- **Gunicorn** - WSGI-сервер для продакшена
- **Nginx** (опционально) - Обратный прокси

## 🗄️ Модели данных

### Основная модель - Habit (Привычка)

```python
class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    place = models.CharField(max_length=255, verbose_name='Место выполнения')
    time = models.TimeField(verbose_name='Время выполнения')
    action = models.CharField(max_length=500, verbose_name='Действие')
    is_pleasant = models.BooleanField(default=False, verbose_name='Приятная привычка')
    related_habit = models.ForeignKey('self', on_delete=models.SET_NULL, 
                                      null=True, blank=True, verbose_name='Связанная привычка')
    frequency = models.PositiveIntegerField(default=1, verbose_name='Периодичность (в днях)')
    reward = models.CharField(max_length=255, blank=True, verbose_name='Вознаграждение')
    duration = models.PositiveIntegerField(validators=[MaxValueValidator(120)], 
                                         verbose_name='Время на выполнение (секунды)')
    is_public = models.BooleanField(default=False, verbose_name='Публичная привычка')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### Модель для Telegram-интеграции

```python
class TelegramUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telegram_id = models.CharField(max_length=100, unique=True)
    chat_id = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

## 🚀 Установка и запуск

### Локальная установка

1. **Клонирование репозитория**
```bash
git clone https://github.com/yourusername/habit-tracker.git
cd habit-tracker
```

2. **Установка Poetry**
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

3. **Установка зависимостей**
```bash
poetry install
```

4. **Активация виртуального окружения**
```bash
poetry shell
```

5. **Настройка базы данных**
```bash
# Создание базы данных PostgreSQL
sudo -u postgres psql
CREATE DATABASE habit_tracker;
CREATE USER habit_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE habit_tracker TO habit_user;
\q
```

6. **Применение миграций**
```bash
python manage.py migrate
```

7. **Создание суперпользователя**
```bash
python manage.py createsuperuser
```

8. **Запуск Redis (для Celery)**
```bash
# Установка Redis
sudo apt-get install redis-server
# Или через Docker
docker run -d -p 6379:6379 redis:alpine
```

9. **Запуск Celery Worker**
```bash
celery -A config worker --loglevel=info
```

10. **Запуск Celery Beat (для периодических задач)**
```bash
celery -A config beat --loglevel=info
```

11. **Запуск сервера разработки**
```bash
python manage.py runserver
```

### Docker-развертывание

1. **Клонирование и настройка**
```bash
git clone https://github.com/yourusername/habit-tracker.git
cd habit-tracker
cp .env.example .env
# Отредактируйте .env файл
```

2. **Запуск контейнеров**
```bash
docker-compose up -d --build
```

3. **Применение миграций**
```bash
docker-compose exec web python manage.py migrate
```

4. **Создание суперпользователя**
```bash
docker-compose exec web python manage.py createsuperuser
```

5. **Сбор статических файлов**
```bash
docker-compose exec web python manage.py collectstatic --noinput
```

6. **Мониторинг логов**
```bash
# Все сервисы
docker-compose logs -f

# Только веб-сервер
docker-compose logs -f web

# Только Celery
docker-compose logs -f celery_worker
```

### Настройка переменных окружения

Создайте файл `.env` в корневой директории:

```env
# Django
SECRET_KEY=django-insecure-your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# База данных
DB_ENGINE=django.db.backends.postgresql
DB_NAME=habit_tracker
DB_USER=habit_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432

# Redis для Celery
REDIS_URL=redis://localhost:6379/0

# Telegram
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Время жизни токена (опционально)
ACCESS_TOKEN_LIFETIME=86400
REFRESH_TOKEN_LIFETIME=604800
```

## 📡 API Endpoints

### Аутентификация
| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | `/api/auth/register/` | Регистрация нового пользователя |
| POST | `/api/auth/login/` | Авторизация (получение токена) |
| POST | `/api/auth/refresh/` | Обновление access токена |
| POST | `/api/auth/logout/` | Выход (аннулирование токена) |

### Привычки
| Метод | Endpoint | Описание | Аутентификация |
|-------|----------|----------|----------------|
| GET | `/api/habits/` | Список привычек пользователя | ✅ |
| POST | `/api/habits/` | Создание новой привычки | ✅ |
| GET | `/api/habits/{id}/` | Детали привычки | ✅ |
| PUT | `/api/habits/{id}/` | Обновление привычки | ✅ |
| PATCH | `/api/habits/{id}/` | Частичное обновление | ✅ |
| DELETE | `/api/habits/{id}/` | Удаление привычки | ✅ |
| GET | `/api/habits/public/` | Список публичных привычек | ❌ |

### Telegram
| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | `/api/telegram/connect/` | Подключение Telegram аккаунта |
| POST | `/api/telegram/disconnect/` | Отключение Telegram |
| GET | `/api/telegram/status/` | Статус подключения |

## 🤖 Интеграция с Telegram

### Настройка Telegram бота

1. **Создание бота через BotFather**
   - Откройте Telegram, найдите @BotFather
   - Отправьте команду `/newbot`
   - Следуйте инструкциям, чтобы задать имя и username бота
   - Сохраните полученный токен в переменную окружения `TELEGRAM_BOT_TOKEN`

2. **Получение chat_id**
   - Пользователь отправляет команду `/start` вашему боту
   - Бот автоматически сохраняет chat_id в базу данных
   - Система начинает отправлять уведомления

### Пример уведомления

```python
# celery/tasks.py
from celery import shared_task
from datetime import datetime
import requests

@shared_task
def send_habit_reminders():
    habits = Habit.objects.filter(time__hour=datetime.now().hour,
                                  time__minute=datetime.now().minute)
    
    for habit in habits:
        if habit.user.telegram_user.exists():
            telegram_user = habit.user.telegram_user.first()
            message = f"⏰ Напоминание о привычке!\n\n" \
                     f"Действие: {habit.action}\n" \
                     f"Время: {habit.time.strftime('%H:%M')}\n" \
                     f"Место: {habit.place}\n" \
                     f"Длительность: {habit.duration} секунд"
            
            requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                json={
                    "chat_id": telegram_user.chat_id,
                    "text": message,
                    "parse_mode": "HTML"
                }
            )
```

## ✅ Валидация данных

Система включает следующие валидаторы:

### 1. Валидаторы моделей
```python
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_habit_creation(habit):
    """Основная валидация создания привычки"""
    errors = []
    
    # Правило 1: Заполнено только одно из полей
    if habit.reward and habit.related_habit:
        errors.append(_("Нельзя указывать одновременно и вознаграждение, и связанную привычку"))
    
    # Правило 2: Время выполнения <= 120 секунд
    if habit.duration > 120:
        errors.append(_("Время выполнения не может превышать 120 секунд"))
    
    # Правило 3: Связанная привычка должна быть приятной
    if habit.related_habit and not habit.related_habit.is_pleasant:
        errors.append(_("Связанная привычка должна быть приятной"))
    
    # Правило 4: У приятной привычки нет вознаграждения или связанной привычки
    if habit.is_pleasant and (habit.reward or habit.related_habit):
        errors.append(_("У приятной привычки не может быть вознаграждения или связанной привычки"))
    
    # Правило 5: Периодичность 1-7 дней
    if habit.frequency < 1 or habit.frequency > 7:
        errors.append(_("Периодичность должна быть от 1 до 7 дней"))
    
    if errors:
        raise ValidationError(errors)
```

### 2. Сериализаторы с валидацией
```python
from rest_framework import serializers

class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')
    
    def validate(self, data):
        # Проверка всех бизнес-правил
        if data.get('reward') and data.get('related_habit'):
            raise serializers.ValidationError(
                "Можно указать только одно: вознаграждение ИЛИ связанную привычку"
            )
        
        if data.get('duration', 0) > 120:
            raise serializers.ValidationError(
                "Время выполнения не может превышать 120 секунд"
            )
        
        return data
```

## 🧪 Тестирование

### Запуск тестов
```bash
# Все тесты
python manage.py test

# Конкретное приложение
python manage.py test habits

# С покрытием кода
coverage run manage.py test
coverage report
coverage html  # для HTML отчета
```

## 🌐 Деплоймент

### Подготовка к продакшену

1. **Настройка production окружения**
```python
# config/settings/production.py
from .base import *

DEBUG = False

ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

# Настройки безопасности
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
```

2. **Docker Compose для продакшена**
```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    env_file:
      - .env.prod
    restart: always

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    restart: always

  web:
    build:
      context: .
      dockerfile: Dockerfile.prod
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - static_volume:/app/staticfiles
    env_file:
      - .env.prod
    depends_on:
      - postgres
      - redis
    restart: always

  celery_worker:
    build:
      context: .
      dockerfile: Dockerfile.prod
    command: celery -A config worker --loglevel=info
    env_file:
      - .env.prod
    depends_on:
      - redis
      - postgres
    restart: always

  celery_beat:
    build:
      context: .
      dockerfile: Dockerfile.prod
    command: celery -A config beat --loglevel=info
    env_file:
      - .env.prod
    depends_on:
      - redis
      - postgres
    restart: always

  nginx:
    image: nginx:1.25-alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/staticfiles
      - ./certbot/conf:/etc/letsencrypt
      - ./certbot/www:/var/www/certbot
    depends_on:
      - web
    restart: always

volumes:
  postgres_data:
  redis_data:
  static_volume:
```
