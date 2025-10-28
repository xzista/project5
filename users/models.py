from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(
        max_length=35, verbose_name="Телефон", blank=True, null=True, help_text="Введите номер телефона"
    )
    tg_nik = models.CharField(max_length=50, verbose_name="TG", help_text="Укажите TG ник", blank=True, null=True)
    avatar = models.ImageField(upload_to="users/avatars/", blank=True, null=True, help_text="Загрузите свой аватар")
    tg_chat_id = models.CharField(
        max_length=50, verbose_name="TG chat_id", help_text="Укажите TG chat_id", blank=True, null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
