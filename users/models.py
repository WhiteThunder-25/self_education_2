from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email", help_text="Введите email")
    first_name = models.CharField(max_length=30, blank=True, null=True, verbose_name="Имя", help_text="Ваше имя")
    last_name = models.CharField(max_length=30, blank=True, null=True, verbose_name="Фамилия", help_text="Ваша фамилия")
    phone_number = PhoneNumberField(max_length=12, blank=True, null=True, verbose_name="Телефон", help_text="Ваш номер телефона")
    avatar = models.ImageField(upload_to="users/avatars/", blank=True, null=True, verbose_name="Аватар", help_text="Ваше фото")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
