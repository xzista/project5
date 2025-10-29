from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .apps import HabitsConfig
from .services import telegram_webhook
from .views import HabitViewSet

app_name = HabitsConfig.name

router = DefaultRouter()
router.register(r"habits", HabitViewSet, basename="habit")

urlpatterns = [
    path("", include(router.urls)),
    path("webhook/", telegram_webhook, name="telegram_webhook"),
]
