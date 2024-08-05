from django.contrib import admin

from coaching.models.applications import Status, Application
from coaching.models.coaching import TeacherGame, Coaching
from coaching.models.games import Game, GameGenre


@admin.register(GameGenre)
class GameGenre(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'genre')


@admin.register(TeacherGame)
class TeacherGameAdmin(admin.ModelAdmin):
    list_display = ('id', 'teacher', 'game')


@admin.register(Coaching)
class CoachingAdmin(admin.ModelAdmin):
    list_display = ('id', 'teacher', 'learner')


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'game', 'status')
