from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from common.permissions.user import IsUserAccount, IsAdmin
from common.views.pagination import BasePagination
from users.serializers.users import UserRegistrationSerializer, UserListAndDetail, ChangePasswordSerializer, \
    PartialUpdateUserSerializer
from common.views.mixins import RUDViewSet
from rest_framework.status import HTTP_201_CREATED

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
class UserRegistration(RUDViewSet):
    multi_serializer_class = {
        'registration': UserRegistrationSerializer,
        'list': UserListAndDetail,
        'retrieve': UserListAndDetail,
        'destroy': UserListAndDetail,
        'change_password': ChangePasswordSerializer,
        'partial_update': PartialUpdateUserSerializer,
    }

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
        return Response(user_serializer.data, status=HTTP_201_CREATED)

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
        )
