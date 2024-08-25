import django_filters
from rest_framework import filters
from django.contrib.auth import get_user_model
from django.db.models import Max, Case, When

from users.constants import positions

User = get_user_model()


class TeacherFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        """
        Работает таким образом, что если не указана конкретная игра, то
        сортировка происходит по максимальному/минимальному полю из всех игр тренера.
        """
        game = request.query_params.get('game')
        queryset = User.objects.filter(
            position=positions.TEACHER_CODE
        ).prefetch_related(
            'teachers_game', 'teachers_game__game'
        )

        if not game:
            queryset = queryset.annotate(
                rating=Max('teachers_game__rating')
            )
        else:
            queryset = queryset.filter(
                teachers_game__game__name=game
            ).annotate(
                rating=Case(
                    When(teachers_game__game__name=game, then='teachers_game__rating'),
                )
            )
        return queryset


class TeacherFilterSet(django_filters.FilterSet):
    game = django_filters.CharFilter(field_name='games_taught__name', lookup_expr='exact')

    class Meta:
        model = User
        fields = ('game',)
