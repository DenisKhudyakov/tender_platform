from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'null': True, 'blank': True}


class User(AbstractUser):
    """
    Класс пользователя, пользователь может быть поставщиком или сотрудником
    """
    username = None
    email = models.EmailField(unique=True)
    company_name = models.CharField(max_length=255, **NULLABLE)
    phone = models.CharField(max_length=20, **NULLABLE)
    inn = models.CharField(max_length=12, **NULLABLE)
    is_employer = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
