import django_filters
from rest_framework import filters
from django.contrib.auth import get_user_model
from django.db.models import Subquery, OuterRef, Max, Case, When

from coaching.models.games import Game

User = get_user_model()


class TeacherQSFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        """
        Работает таким образом, что если не указана конкретная игра, то
        сортировка происходит по максимальному рейтингу из всех игр тренера.
        """
        qs = User.objects.annotate(
            rating=Max('teachers_game__rating')
        )
        game = request.query_params.get('game')
        if game:
            qs = qs.filter(
                teachers_game__game__name=game
            ).annotate(
                rating=Case(
                    When(teachers_game__game__name=game, then='teachers_game__rating'),
                )
            )
        return qs


class TeacherFilter(django_filters.FilterSet):
    game = django_filters.CharFilter(field_name='games_taught__name', lookup_expr='exact')

    class Meta:
        model = User
        fields = ('game',)


