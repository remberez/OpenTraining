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
    position = models.ForeignKey(
        'Position', verbose_name='Должность',
        related_name='users', on_delete=models.RESTRICT,
        null=True,
    )
    name = models.CharField(
        verbose_name='Имя', max_length=25,
    )

    # Модели профиля будут иметь username и name
    # username - что-то вроде id аккаунта как в телеграмме,
    # name - конкретное, отображаемое имя на странице пользователя.

    image = models.ImageField(
        upload_to='users/%Y/%m/%d/', null=True, blank=True,
    )
    date_joined = models.DateField(auto_now=True, editable=True)
    games_taught = models.ManyToManyField(
        'coaching.Game', verbose_name='Преподаваемые игры',
        related_name='game_teachers', through='coaching.TeacherGame',
    )
    learning_games = models.ManyToManyField(
        'coaching.TeacherGame', verbose_name='Игры ученика',
        related_name='learner_games', through='coaching.Coaching',
        through_fields=('learner', 'game')
    )

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.username}'
