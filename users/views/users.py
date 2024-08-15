from django.contrib.auth import get_user_model
from django.db.models import Case, When
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from common.permissions.user import IsUserAccount, IsAdmin
from common.views.pagination import BasePagination
from users.constants.positions import LEARNER_CODE
from users.filters import UserFilter
from users.constants.positions import TEACHER_CODE
from users.serializers import users
from common.views.mixins import RUDViewSet
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

User = get_user_model()


@extend_schema_view(
    registration=extend_schema(
        summary='Регистрация',
        tags=['Пользователи']
    ),
    list=extend_schema(
        summary='Получить данные о пользователях',
        tags=['Пользователи'],
    ),
    retrieve=extend_schema(
        summary='Получить данные о пользователе',
        tags=['Пользователи'],
    ),
    partial_update=extend_schema(
        summary='Изменить данные о пользователе',
        tags=['Управление аккаунтом'],
    ),
    destroy=extend_schema(
        summary='Удалить пользователя',
        tags=['Управление аккаунтом'],
    ),
    change_password=extend_schema(
        summary='Смена пароля',
        tags=['Управление аккаунтом'],
    )
)
class UserView(RUDViewSet):
    multi_serializer_class = {
        'registration': users.UserRegistrationSerializer,
        'list': users.UserListAndDetail,
        'retrieve': users.UserListAndDetail,
        'change_password': users.ChangePasswordSerializer,
        'partial_update': users.PartialUpdateUserSerializer,
    }

    filter_backends = (
        SearchFilter,
        OrderingFilter,
        DjangoFilterBackend,
    )
    filterset_class = UserFilter

    search_fields = ('username',)
    ordering_fields = ('username', 'pk')
    ordering = ('username',)

    queryset = User.objects.all()
    http_method_names = ('get', 'post', 'delete', 'patch')

    multi_permission_classes = {
        'registration': (AllowAny,),
        'destroy': (IsUserAccount | IsAdmin,),
        'partial_update': (IsUserAccount | IsAdmin,),
    }

    pagination_class = BasePagination

    @action(methods=['post'], detail=False)
    def registration(self, request):
        serializer = self.get_serializer_class()
        user_serializer = serializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        return Response(user_serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=['patch'], detail=False)
    def change_password(self, request):
        serializer = self.get_serializer_class()
        password_serializer = serializer(instance=request.user, data=request.data)
        password_serializer.is_valid(raise_exception=True)
        password_serializer.save()
        return Response(status=HTTP_204_NO_CONTENT)

    def get_queryset(self):
        return User.objects.select_related(
            'learner_profile'
        ).select_related(
            'teacher_profile'
        ).annotate(
            is_teacher=Case(
                When(position=TEACHER_CODE, then=True), default=False,
            )
        )

    def destroy(self, request, *args, **kwargs):
        # Пользователь не может удалить свой аккаунт, если занимает какую-либо должность.
        instance = self.get_object()
        if instance.position.code != LEARNER_CODE:
            return Response(status=status.HTTP_403_FORBIDDEN, data="Обратитесь к администратору.")
        return super().destroy(request, *args, **kwargs)
    