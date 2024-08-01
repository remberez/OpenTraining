from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from users.serializers import users
from rest_framework.viewsets import ModelViewSet, GenericViewSet

User = get_user_model()


@extend_schema_view(
    create=extend_schema(
        summary='Регистрация пользователя',
        tags=['Регистрация'],
    ),
    retrieve=extend_schema(
        summary='Информация о пользователе',
        tags=['Информация'],
    ),
    list=extend_schema(
        summary='Список пользователей',
        tags=['Информация'],
    ),
    partial_update=extend_schema(
        summary="Изменение данных пользователя",
        tags=['Управление аккаунтом'],
    )
)
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = users.UserSerializer
    http_method_names = ('get', 'post', 'patch')

    def get_serializer_context(self):
        """
        Передача запроса в UserSerializer
        """
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_update(self, serializer):
        user = self.get_object()
        print(user, self.request.user)
        if user != self.request.user:
            raise PermissionDenied("У вас нет прав для изменения этого аккаунта.")
        serializer.save()


@extend_schema_view(
    change_password=extend_schema(
        summary='Смена пароля',
        tags=['Управление аккаунтом'],
    )
)
class ChangePasswordViewSet(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = users.ChangePasswordSerializer

    @action(
        methods=['post'],
        detail=False,
    )
    def change_password(self, request):
        serializer = self.get_serializer_class()
        password_serializer = serializer(instance=request.user, data=request.data)
        password_serializer.is_valid(raise_exception=True)
        password_serializer.save()
        return Response(status=HTTP_204_NO_CONTENT)
