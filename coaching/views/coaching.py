from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.response import Response
from common.views.mixins import ListRetrieveViewSet, CreateViewSet
from coaching.models.coaching import Coaching
from coaching.serializers import coaching
from rest_framework import status
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter
from common.permissions.user import IsUserAccount, IsAdmin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from coaching.backends.coaching import CoachingFilter, CoachingSearchFilter
from common.views.pagination import BasePagination
from rest_framework.permissions import IsAuthenticated

User = get_user_model()


@extend_schema_view(
    list=extend_schema(
        summary='Список всех наставничеств',
        tags=['Тренерство'],
        parameters=[
            OpenApiParameter(
                'include_teacher', type=bool, required=False,
                description='Если false, то не будет включено поле с преподаваемыми играми.',
            ),
            OpenApiParameter(
                'include_learner', type=bool, required=False,
                description='По аналогии.'
            ),
        ]
    ),
    retrieve=extend_schema(
        summary='Детальная информация о наставничестве',
        tags=['Тренерство'],
    ),
    user_coaching=extend_schema(
        summary='Детальная информация о наставничестве пользователя',
        tags=['Тренерство']
    )
)
class UserCoachingView(ListRetrieveViewSet):
    queryset = User.objects.all()
    multi_serializer_class = {
        'list': coaching.UserCoachingSerializer,
        'user_coaching': coaching.UserCoachingSerializer,
    }
    multi_permission_classes = {
        'user_coaching': [IsUserAccount | IsAdmin],
    }

    filter_backends = (
        OrderingFilter,
        CoachingFilter,
        DjangoFilterBackend,
    )

    ordering = ('pk',)
    pagination_class = BasePagination
    filterset_class = CoachingSearchFilter

    @action(detail=True, methods=['get'])
    def user_coaching(self, request, *args, **kwargs):
        user = self.get_object()
        return Response(status=status.HTTP_200_OK, data=self.get_serializer(user).data)


@extend_schema_view(
    create=extend_schema(
        summary='Создать заявку на начало тренерства',
        tags=['Тренерство'],
        description='Работает так, что заявку может отправить как и тренер, '
                    'так и ученик. Принять её должен получатель, тогда создаться '
                    'наставничество.'
    )
)
class CoachingView(CreateViewSet):
    queryset = Coaching.objects.all()

    multi_serializer_class = {
        'create': coaching.StartCoachingSerializer,
    }

    multi_permission_classes = {
        'create': [IsAuthenticated]
    }
