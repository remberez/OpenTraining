from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Coaching(models.Model):
    teacher = models.ForeignKey(
        User, verbose_name='Учитель',
        on_delete=models.CASCADE, related_name='teacher_coaching'
    )
    learner = models.ForeignKey(
        User, verbose_name='Ученик',
        on_delete=models.CASCADE, related_name='learner_coaching'
    )
    game = models.ForeignKey(
        'TeacherGame', verbose_name='Игра',
        on_delete=models.CASCADE, related_name='coaching',
    )
    start_coaching = models.DateField(blank=True, null=True, verbose_name='Начало')
    end_coaching = models.DateField(blank=True, null=True, verbose_name='Конец')
    is_active = models.BooleanField(default=False, verbose_name='Активность наставничества')
    learner_comment = models.TextField(verbose_name='Комментарий ученика')
    teacher_consent = models.BooleanField(verbose_name='Согласие тренера')
    learner_consent = models.BooleanField(verbose_name='Согласие ученика')

    class Meta:
        verbose_name = 'Учитель - ученик'
        verbose_name_plural = 'Учителя - ученики'


class TeacherGame(models.Model):
    teacher = models.ForeignKey(
        User, verbose_name='Учитель',
        on_delete=models.CASCADE, related_name='teachers_game'
    )
    game = models.ForeignKey(
        'coaching.Game', verbose_name='Игра',
        on_delete=models.RESTRICT, related_name='teachers',
    )
    description = models.TextField(null=True, blank=True)
    date_created = models.DateField(auto_now=True)
    price = models.FloatField(null=True, blank=True)
    rating = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = 'Игры учителя'
        verbose_name_plural = 'Игры учителей'

    def __str__(self):
        return f'{self.teacher} - {self.game}'
