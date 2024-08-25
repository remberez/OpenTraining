import django_filters
from coaching.models.games import Game


class GameFilter(django_filters.FilterSet):
    genre = django_filters.CharFilter('genre__name', lookup_expr='exact')

    class Meta:
        model = Game
        fields = ('genre', 'name')
