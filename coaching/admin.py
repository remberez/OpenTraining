from django.contrib import admin

from coaching.models.coaching import TeacherGame, Coaching
from coaching.models.games import Game


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )


@admin.register(TeacherGame)
class TeacherGameAdmin(admin.ModelAdmin):
    list_display = ('id', 'teacher', 'game')


@admin.register(Coaching)
class CoachingAdmin(admin.ModelAdmin):
    list_display = ('id', 'teacher', 'learner')
