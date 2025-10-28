# Set the default Django settings module for the 'celery' program.
import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Beat
app.conf.beat_schedule = {
    'send-habit-reminders-every-minute': {
        'task': 'notifications.tasks.send_habit_reminders',
        'schedule': crontab(minute='*'),  # можно заменить на "*/10" для каждых 10 минут
    },
}

app.conf.timezone = 'Europe/Moscow'
app.conf.enable_utc = False

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')