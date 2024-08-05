from django.db import models


class Position(models.Model):
    code = models.CharField(verbose_name='Код', max_length=32, primary_key=True)
    name = models.CharField(verbose_name='Название должности', max_length=32)

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'

    def __str__(self):
        return f'{self.code} {self.name}'
