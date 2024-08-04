from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from users.models.profiles import Teacher, Learner
from users.models.users import User


class TeacherProfileAdmin(admin.TabularInline):
    model = Teacher
    extra = 0


class LearnerProfileAdmin(admin.TabularInline):
    model = Learner
    extra = 0


@admin.register(User)
class UserAdmin(UserAdmin):
    change_user_password_template = None
    fieldsets = (
        (None, {'fields': ('username', 'discord_id', 'email', 'is_public', 'is_admin', 'is_teacher')}),
        (_('Личная информация'),
         {'fields': ('first_name', 'last_name',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'discord_id', 'password1', 'password2',),
        }),
    )
    list_display = ('id', 'username', 'email', 'discord_id', )
    list_display_links = ('username', )
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('first_name', 'last_name', 'id', 'email', 'discord_id',)
    ordering = ('-id',)
    filter_horizontal = ('groups', 'user_permissions',)
    readonly_fields = ('last_login',)
    inlines = (TeacherProfileAdmin, LearnerProfileAdmin)