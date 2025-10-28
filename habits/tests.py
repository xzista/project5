from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from habits.models import Habit

User = get_user_model()


class HabitModelTest(TestCase):
    """Тесты модели Habit"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.user = User.objects.create(
            email="test@example.com",
            is_active=True
        )
        self.user.set_password("testpass123")
        self.user.save()

        self.pleasant_habit = Habit.objects.create(
            owner=self.user,
            place="Дом",
            time="08:00:00",
            action="Утренняя медитация",
            is_pleasant=True,
            duration_seconds=120
        )

    def test_create_habit(self):
        """Тест создания привычки"""
        habit = Habit.objects.create(
            owner=self.user,
            place="Парк",
            time="07:00:00",
            action="Бег",
            is_pleasant=False,
            duration_seconds=60,
            period_days=2
        )

        self.assertEqual(habit.owner, self.user)
        self.assertEqual(habit.place, "Парк")
        self.assertEqual(habit.action, "Бег")
        self.assertFalse(habit.is_pleasant)
        self.assertEqual(habit.duration_seconds, 60)
        self.assertEqual(habit.period_days, 2)

    def test_pleasant_habit_validation(self):
        """Тест валидации приятной привычки"""
        habit = Habit(
            owner=self.user,
            place="Дом",
            time="09:00:00",
            action="Чтение книги",
            is_pleasant=True,
            reward_text="Кофе"
        )

        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_duration_validation(self):
        """Тест валидации времени выполнения"""
        habit = Habit(
            owner=self.user,
            place="Дом",
            time="10:00:00",
            action="Тестовая привычка",
            duration_seconds=121
        )

        with self.assertRaises(ValidationError):
            habit.full_clean()

    def test_habit_string_representation(self):
        """Тест строкового представления"""
        habit = Habit.objects.create(
            owner=self.user,
            place="Кухня",
            time="08:30:00",
            action="Завтрак",
            is_pleasant=True
        )

        self.assertIn("Завтрак", str(habit))
        self.assertIn("приятная", str(habit))


class HabitViewSetTest(APITestCase):
    """Тесты HabitViewSet API"""

    def setUp(self):
        """Настройка тестовых данных"""
        self.user = User.objects.create(
            email="user@example.com",
            is_active=True
        )
        self.user.set_password("testpass123")
        self.user.save()

        self.other_user = User.objects.create(
            email="other@example.com",
            is_active=True
        )
        self.other_user.set_password("testpass123")
        self.other_user.save()

        self.habit_private = Habit.objects.create(
            owner=self.user,
            place="Дом",
            time="08:00:00",
            action="Медитация",
            is_pleasant=True,
            is_public=False
        )
        self.habit_public = Habit.objects.create(
            owner=self.user,
            place="Парк",
            time="07:00:00",
            action="Бег",
            is_pleasant=False,
            is_public=True
        )

        self.client = APIClient()

    def test_list_habits_authenticated(self):
        """Тест получения списка привычек аутентифицированным пользователем"""
        self.client.force_authenticate(user=self.user)
        url = reverse("habits:habit-list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        habits_count = len(response.data["results"])
        self.assertEqual(habits_count, 2)

    def test_create_habit(self):
        """Тест создания привычки"""
        self.client.force_authenticate(user=self.user)
        url = reverse("habits:habit-list")
        data = {
            "place": "Офис",
            "time": "12:00:00",
            "action": "Обеденная прогулка",
            "is_pleasant": True,
            "duration_seconds": 90,
            "period_days": 1
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 3)
        self.assertEqual(Habit.objects.last().owner, self.user)

    def test_retrieve_own_habit(self):
        """Тест получения своей привычки"""
        self.client.force_authenticate(user=self.user)
        url = reverse("habits:habit-detail", kwargs={"pk": self.habit_private.id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["action"], "Медитация")

    def test_update_own_habit(self):
        """Тест обновления своей привычки"""
        self.client.force_authenticate(user=self.user)
        url = reverse("habits:habit-detail", kwargs={"pk": self.habit_private.id})
        data = {
            "place": "Новое место",
            "time": "09:00:00",
            "action": "Обновленная медитация",
            "is_pleasant": True,
            "duration_seconds": 120
        }

        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit_private.refresh_from_db()
        self.assertEqual(self.habit_private.action, "Обновленная медитация")

    def test_delete_own_habit(self):
        """Тест удаления своей привычки"""
        self.client.force_authenticate(user=self.user)
        url = reverse("habits:habit-detail", kwargs={"pk": self.habit_private.id})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 1)

    def test_public_habits_endpoint(self):
        """Тест эндпоинта публичных привычек"""
        url = reverse("habits:habit-public")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        public_habits = [h for h in response.data["results"] if h["is_public"]]
        self.assertTrue(len(public_habits) > 0)
