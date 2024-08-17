from django.db.models import Count
from drf_spectacular.utils import extend_schema_view, OpenApiParameter
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema
from coaching.backends import GameCustomSearchFilter
from coaching.models.games import Game, GameGenre
from common.permissions.user import IsAdmin
from common.views.mixins import CRUDViewSet
from coaching.serializers.games import *
from common.views.pagination import BasePagination
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


@extend_schema_view(
    list=extend_schema(
        summary='Все игры',
        tags=['Игры'],
        parameters=[
            OpenApiParameter(
                name='genre',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Фильтрация игр по жанру',
            ),
        ],
    ),
    retrieve=extend_schema(
        summary='Игра',
        tags=['Игры']
    ),
    destroy=extend_schema(
        summary='Удалить игру',
        tags=['Игры']
    ),
    partial_update=extend_schema(
        summary='Изменить данные об игре',
        tags=['Игры']
    ),
    create=extend_schema(
        summary='Добавить игру',
        tags=['Игры']
    ),
    short_info_list=extend_schema(
        summary='Список с короткой информацией об играх',
        tags=['Игры'],
        filters=True
    )
)
class GameView(CRUDViewSet):
    multi_serializer_class = {
        'retrieve': GameListAndRetrieveSerializer,
        'list': GameListAndRetrieveSerializer,
        'create': CreateGameSerializer,
        'destroy': DeleteGameSerializer,
        'partial_update': GameUpdateSerializer,
        'short_info_list': GameShortSerializer,
    }

    multi_permission_classes = {
        'retrieve': [AllowAny],
        'list': [AllowAny],
        'destroy': [IsAdmin],
        'partial_update': [IsAdmin],
        'create': [IsAdmin],
    }

    queryset = Game.objects.all()
    http_method_names = ('get', 'post', 'patch', 'delete')
    pagination_class = BasePagination

    filter_backends = (
        OrderingFilter,
        DjangoFilterBackend,
        GameCustomSearchFilter,
    )

    search_fields = ('name', 'description',)
    ordering_fields = ('name', 'pk')
    ordering = ('pk',)

    @action(
        methods=['get'], detail=False,
    )
    def short_info_list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        return Game.objects.annotate(
                    count_teachers=Count(
                        'teachers', distinct=True,
                    )
                )


@extend_schema_view(
    list=extend_schema(
        summary='Список жанров',
        tags=['Жанры'],
    ),
    retrieve=extend_schema(
        summary='Жанр детально',
        tags=['Жанры'],
    ),
    partial_update=extend_schema(
        summary='Обновить жанр',
        tags=['Жанры'],
    ),
    destroy=extend_schema(
        summary='Удалить жанр',
        tags=['Жанры'],
    ),
    create=extend_schema(
        summary='Добавить жанр',
        tags=['Жанры'],
    ),

)
class GameGenreView(CRUDViewSet):
    multi_serializer_class = {
        'list': GameGenreRetrieveListSerializer,
        'retrieve': GameGenreRetrieveListSerializer,
        'create': GameGenreCreateSerializer,
        'partial_update': GameGenreUpdateSerializer,
        'destroy': GameGenreDestroySerializer,
    }

    multi_permission_classes = {
        'retrieve': [AllowAny],
        'list': [AllowAny],
        'destroy': [IsAdmin],
        'partial_update': [IsAdmin],
        'create': [IsAdmin],
    }

    queryset = GameGenre.objects.all()
    http_method_names = ('get', 'post', 'patch', 'delete')
    pagination_class = BasePagination
