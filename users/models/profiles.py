from django.db import models


class BaseProfile(models.Model):
    # Базовая абстрактная модель для профиля
    name = models.CharField(
        verbose_name='Имя', max_length=25,
    )
    # Модели профиля будут иметь username и name
    # username - что-то вроде id аккаунта как в телеграмме,
    # name - конкретное, отображаемое имя на странице пользователя.
    image = models.ImageField(
        upload_to='users/%Y/%m/%d/', null=True, blank=True,
    )
    account_lvl = models.PositiveSmallIntegerField(
        default=1
    )
    date_joined = models.DateField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.name}'


"""
Две модели профиля созданы для возможности
удобно расширять код. Например добавлять 
в профиль учителя то, чего не должно быть
в профиле у ученика.
"""


class Learner(BaseProfile):
    user = models.OneToOneField(
        'users.User', verbose_name='Пользователь',
        related_name='learner_profile', on_delete=models.CASCADE
    )


class Teacher(BaseProfile):
    user = models.OneToOneField(
        'users.User', verbose_name='Пользователь',
        related_name='teacher_profile', on_delete=models.CASCADE
    )
    games = models.ManyToManyField(
        'coaching.Game', verbose_name='Преподаваемые игры',
        related_name='game_teachers', through='coaching.TeacherGame',
    )
