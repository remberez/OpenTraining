from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Status(models.Model):
    code = models.CharField(
        verbose_name='Код', max_length=32, primary_key=True,
    )
    name = models.CharField(
        verbose_name='Статус заявки', max_length=32,
    )

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'

    def __str__(self):
        return self.name


class Application(models.Model):
    sender = models.ForeignKey(
        User, verbose_name='Отправитель заявки',
        related_name='submitted_applications', on_delete=models.CASCADE,
    )
    manager = models.ForeignKey(
        User, verbose_name='Рассматривающий заявку', null=True, blank=True,
        related_name='accepted_applications', on_delete=models.SET_NULL,
    )
    about_sender = models.TextField(verbose_name='Информация об отправителе')
    created_at = models.DateTimeField(
        verbose_name='Дата создания заявки', auto_now=True, editable=True
    )
    accepted_at = models.DateTimeField(
        null=True, blank=True, verbose_name='Дата принятия заявки'
    )
    status = models.ForeignKey(
        'Status', verbose_name='Статус заявки',
        related_name='applications', on_delete=models.RESTRICT,
    )
    sender_discord = models.CharField(
        verbose_name='Дискорд отправителя', max_length=32,
    )
    full_name = models.CharField(
        verbose_name='Полное имя отправителя', max_length=64,
    )
    game = models.ForeignKey(
        'Game', verbose_name='Игра', null=True,
        related_name='applications', on_delete=models.SET_NULL,
    )
    rating = models.CharField(
        max_length=32, verbose_name='Рейтинг отправителя',
    )

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return f'{self.sender}, {self.game}'
