from django.db import models


class Game(models.Model):
    name = models.CharField(
        verbose_name='Название игры', max_length=32,
    )
    description = models.TextField(
        verbose_name='Описание игры',
    )
    image = models.ImageField(
        upload_to='games/%Y/%m/%d/', null=True, blank=True,
    )

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'

    def __str__(self):
        return f'{self.name}'
