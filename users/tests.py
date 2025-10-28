from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User


class UserAPITest(APITestCase):
    def test_register_user(self):
        """Тест регистрации пользователя"""
        url = reverse("users:register")
        data = {
            "email": "test@example.com",
            "password": "1234test",
            "first_name": "Test",
            "last_name": "User"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="test@example.com").exists())

    def test_login_jwt(self):
        """Тест JWT авторизации"""
        user = User.objects.create(
            email="user@example.com",
            is_active=True
        )
        user.set_password("pass1234")
        user.save()

        url = reverse("users:login")
        data = {"email": "user@example.com", "password": "pass1234"}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)