# Веб-приложение на Django REST framework

## Описание проекта
Работа над SPA веб-приложением. Ожидание - бэкенд-сервер, который возвращает клиенту JSON-структуры

Приложение развернуто на http://158.160.206.89:8080/
## 🚀 Установка и запуск локально

1. Клонируйте репозиторий:
```bash
git clone https://github.com/xzista/project5
cd project5
```
2. Установите зависимости:
```bash
poetry install
```
3. Примените миграции:
```bash
python manage.py migrate
```
4. Запустите сервер:
```bash
python manage.py runserver
```

## ⚙️ Настройка CI/CD и деплоя
1. Подготовка сервера
   - Установить зависимости:
   ```
   sudo apt update
   sudo apt install -y docker docker-compose git
   ```
   - Клонировать проект:
   ```
   cd /opt
   sudo git clone https://github.com/xzista/project5.git habit-platform
   cd habit-platform
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
3. GitHub Secrets

Для корректной работы CI/CD необходимо добавить в Settings → Secrets → Actions следующие секреты:

```
Название	        Пример значения	        Назначение

SERVER_HOST	        51.250.xxx.xxx	        IP сервера
SERVER_USER	        ubuntu	                SSH-пользователь
SERVER_SSH_KEY	        приватный SSH-ключ	Подключение к серверу
SECRET_KEY	        django-insecure-abc123	Ключ Django
NAME_DB	                education_db	        Имя БД
USER_DB	postgres	Пользователь            БД
PASSWORD_DB	        strongpassword	        Пароль БД
STRIPE_API_KEY	        sk_test_...	        Ключ Stripe
EMAIL_HOST_USER	        example@yandex.ru       Email
EMAIL_HOST_PASSWORD	app-password	        Пароль почты
TEST_SECRET_KEY	        test-secret-key	        Для тестов
TEST_NAME_DB	        test_db	                Для тестов
TEST_USER_DB	        test_user	        Для тестов
TEST_PASSWORD_DB	test_password	        Для тестов
```