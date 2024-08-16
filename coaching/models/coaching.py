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
    start_coaching = models.DateField(blank=True, null=True)
    end_coaching = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    learner_comment = models.TextField()

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
    description = models.TextField()
    date_created = models.DateField(auto_now=True)
    price = models.FloatField()
    rating = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name = 'Игры учителя'
        verbose_name_plural = 'Игры учителей'

    def __str__(self):
        return f'{self.teacher} - {self.game}'
