from django.db import models


class TeacherGame(models.Model):
    teacher = models.ForeignKey(
        'users.Teacher', verbose_name='Учитель',
        on_delete=models.CASCADE,
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
