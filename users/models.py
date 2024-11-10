from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"null": True, "blank": True}


class User(AbstractUser):
    """
    Класс пользователя, пользователь может быть поставщиком или сотрудником
    """

    username = None
    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Введите электронную почту"
    )
    company_name = models.CharField(
        max_length=255,
        **NULLABLE,
        verbose_name="Название компании",
        help_text="Введите название организации"
    )
    phone = models.CharField(
        max_length=20,
        **NULLABLE,
        verbose_name="Телефонный номер",
        help_text="Введите номер телефона"
    )
    inn = models.CharField(
        max_length=12,
        **NULLABLE,
        verbose_name="ИНН",
        help_text="Введите ИНН организации"
    )
    is_employer = models.BooleanField(
        default=False,
        verbose_name="Сотрудник",
        help_text="Является ли пользователь сотрудником?",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
