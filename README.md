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
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="habits")
    place = models.CharField(max_length=255, blank=True)
    time = models.TimeField()
    action = models.CharField(max_length=255)
    is_pleasant = models.BooleanField(default=False)
    related_habit = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL, related_name="linked_by"
    )
    period_days = models.PositiveSmallIntegerField(default=1)
    reward_text = models.CharField(max_length=255, blank=True, null=True)
    duration_seconds = models.PositiveSmallIntegerField(default=60)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

## 🚀 Установка и запуск

### Локальная установка

1. **Клонирование репозитория**
```bash
git clone https://github.com/xzista/habit-tracker.git
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
SECRET_KEY=

DEBUG=

POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_HOST=
POSTGRES_PORT=

ALLOWED_HOSTS=

TELEGRAM_URL=
TELEGRAM_TOKEN=
```

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


## ✅ Валидация данных

Система включает следующие валидаторы:

### Сериализаторы с валидацией
```python
from rest_framework import serializers


def validate_mutual_exclusion(reward_text, related_habit):
    """
    Нельзя одновременно указывать вознаграждение и связанную привычку.
    """
    if reward_text and related_habit:
        raise serializers.ValidationError("Нельзя одновременно указывать вознаграждение и связанную привычку.")


def validate_duration(duration_seconds):
    """
    Время выполнения не должно превышать 120 секунд.
    """
    if duration_seconds and duration_seconds > 120:
        raise serializers.ValidationError("Время выполнения не должно превышать 120 секунд (2 минуты).")


def validate_periodicity(period_days):
    """
    Периодичность выполнения — от 1 до 7 дней.
    """
    if period_days and not (1 <= period_days <= 7):
        raise serializers.ValidationError("Периодичность выполнения должна быть от 1 до 7 дней.")


def validate_related_habit(related_habit):
    """
    Связанная привычка должна быть приятной.
    """
    if related_habit and not related_habit.is_pleasant:
        raise serializers.ValidationError("Связанная привычка должна быть помечена как приятная (is_pleasant=True).")


def validate_pleasant_habit(is_pleasant, reward_text, related_habit):
    """
    У приятной привычки не может быть вознаграждения или связанной привычки.
    """
    if is_pleasant and (reward_text or related_habit):
        raise serializers.ValidationError("У приятной привычки не может быть вознаграждения или связанной привычки.")
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

1. Подготовка сервера
   - Установить зависимости:
   ```
   sudo apt update
   sudo apt install -y docker docker-compose git
   ```
   - Клонировать проект:
   ```
   cd /opt
   sudo git clone https://github.com/xzista/habit-tracker.git habit-tracker
   cd habit-tracker
   ```
   - Создать .env на основе шаблона:
   ```
   cp .env.sample .env
   ```
   - Запустить проект:
   ```
   docker-compose -f docker-compose.prod.yaml up -d --build
   ```
2. GitHub Actions Workflow
    - Файл workflow находится по пути:
   ```
   .github/workflows/ci.yml
   ```
   - Деплой запускается автоматически при push в ветку main.
