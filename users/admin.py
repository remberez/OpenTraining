from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from users.models.position import Position
from users.models.users import User
from coaching.models.coaching import TeacherGame, Coaching


class PositionAdmin(admin.TabularInline):
    model = Position
    extra = 0


class TeacherGameAdmin(admin.TabularInline):
    model = TeacherGame
    extra = 0


class LearningGameAdmin(admin.TabularInline):
    model = Coaching
    extra = 0
    fk_name = 'learner'


@admin.register(User)
class UserAdmin(UserAdmin):
    change_user_password_template = None
    fieldsets = (
        (None, {'fields': ('username', 'discord_id', 'email', 'is_public', 'position', 'name', 'image',)}),
        (_('Личная информация'),
         {'fields': ('first_name', 'last_name',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'discord_id', 'password1', 'password2',),
        }),
    )
    list_display = ('id', 'username', 'email', 'discord_id', 'date_joined')
    list_display_links = ('username', )
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('first_name', 'last_name', 'id', 'email', 'discord_id',)
    ordering = ('-id',)
    filter_horizontal = ('groups', 'user_permissions',)
    readonly_fields = ('last_login', 'date_joined')
    inlines = (TeacherGameAdmin, LearningGameAdmin)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
