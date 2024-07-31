from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager


class User(AbstractUser):
    username = models.CharField(
        verbose_name='Никнейм', max_length=25,
        unique=True, blank=True,
    )
    email = models.EmailField(
        verbose_name='Почта', unique=True, blank=True, null=True,
    )
    discord_id = models.CharField(
        verbose_name='ID дискорда', unique=True,
        max_length=25, blank=True, null=True,
    )
    is_public = models.BooleanField(default=True)
    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.username}'
