from django.db.models import Count
from drf_spectacular.utils import extend_schema_view
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema
from coaching.models.games import Game
from common.permissions.user import IsAdmin
from common.views.mixins import CRUDViewSet
from coaching.serializers.games import GameListAndRetrieveSerializer, ShortInfoGameSerializer, CreateGameSerializer, \
    DeleteGameSerializer, GameUpdateSerializer
from common.views.pagination import BasePagination
from rest_framework.filters import SearchFilter, OrderingFilter


@extend_schema_view(
    list=extend_schema(
        summary='Все игры',
        tags=['Игры']
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
        'short_info_list': ShortInfoGameSerializer,
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
        SearchFilter,
        OrderingFilter,
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
