from django.db import models


class GameGenre(models.Model):
    name = models.CharField(
        verbose_name='Название жанра', max_length=32
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Game(models.Model):
    name = models.CharField(
        verbose_name='Название игры', max_length=32,
    )
    description = models.TextField(
        verbose_name='Описание игры',
    )
    image = models.ImageField(
        upload_to='games/%Y/%m/%d/', null=True, blank=True,
        verbose_name='Логотип игры'
    )
    genre = models.ForeignKey(
        'GameGenre', related_name='games', verbose_name='Жанр игры',
        null=True, blank=True, on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'

    def __str__(self):
        return f'{self.name}'
