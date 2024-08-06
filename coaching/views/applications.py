from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from coaching.backends import ApplicationFilter
from coaching.models.applications import Application, Status
from coaching.permissions import CanManageApplications
from common.views.mixins import CRDViewSet, CRUDViewSet, UDViewSet, CRViewSet, DestroyViewSet
from coaching.serializers import applications
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.filters import OrderingFilter, SearchFilter
from coaching.constants.statuses import *


@extend_schema_view(
    create=extend_schema(
        summary='Создать заявку на тренерство',
        tags=['Заявки на тренерство'],
        description='Заявку на тренерство может создавать кто угодно,\n'
                    'но может быть только одна активная заявка'
    ),
    list=extend_schema(
        summary='Все заявки на тренерство',
        tags=['Заявки на тренерство'],
        description='Администратор или менеджер могут смотреть все заявки,\n'
                    ' обычные пользователи - только свои.'
    ),
    retrieve=extend_schema(
        summary='Заявка на тренерство детально',
        tags=['Заявки на тренерство'],
        description='Аналогично со списком заявок.'
    ),
    destroy=extend_schema(
        summary='Удалить заявку на тренерство',
        tags=['Заявки на тренерство'],
        description='Удаление может производить только администратор или менеджер.\n'
                    'Так будет лучше т.к. человек не сможет спамить заявками\n'
                    'удаляя и создавая их по новой.'
    ),
)
class ApplicationView(CRViewSet):
    queryset = Application.objects.all()
    http_method_names = ('post', 'get',)

    multi_serializer_class = {
        'create': applications.ApplicationCreateSerializer,
        'list': applications.ApplicationCreateSerializer,
        'retrieve': applications.ApplicationRetrieveSerializer,
    }

    multi_permission_classes = {
        'create': [IsAuthenticated],
        'list': [IsAuthenticated],
        'retrieve': [IsAuthenticated],
    }

    filter_backends = [
        ApplicationFilter,
        OrderingFilter,
        SearchFilter,
    ]
    search_fields = ('full_name',)
    ordering_fields = ('full_name', 'created_at', 'approved_at', 'status')
    ordering = ('created_at',)

    def perform_create(self, serializer):
        # Возможно надо это делать в сериалайзере, но раз уже написал то хуй с ним
        meta_data = {
            'status': Status.objects.filter(code=WAITING_STATUS_CODE).first(),
            'sender': self.request.user,
        }
        serializer.save(**meta_data)

    def create(self, request, *args, **kwargs):
        if self.filter_queryset(self.get_queryset()):
            return Response(status=HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)


@extend_schema_view(
    create=extend_schema(
        summary='Создать статус',
        tags=['Статусы заявок'],
    ),
    list=extend_schema(
        summary='Все статусы',
        tags=['Статусы заявок'],
    ),
    retrieve=extend_schema(
        summary='Статус детально',
        tags=['Статусы заявок'],
    ),
    destroy=extend_schema(
        summary='Удалить статус',
        tags=['Статусы заявок'],
    ),
    partial_update=extend_schema(
        summary='Обновить статус',
        tags=['Статусы заявок'],
    ),
)
class StatusView(CRUDViewSet):
    queryset = Status.objects.all()
    serializer_class = applications.StatusCRUSerializer
    http_method_names = ('post', 'get', 'delete', 'patch')

    multi_serializer_class = {
        'destroy': applications.StatusDeleteSerializer
    }
    permission_classes = [IsAdminUser]
    
    base_cods = [
        WAITING_STATUS_CODE,
        PROCESSING_STATUS_CODE,
        APPROVED_STATUS_CODE,
        ACCEPTED_STATUS_CODE,
    ]
    
    def destroy(self, request, *args, **kwargs):
        code = kwargs.get('pk')
        if code and code in self.base_cods:
            return Response(status=HTTP_400_BAD_REQUEST, data='Невозможно удалить данный статус')
        return super().destroy(request, *args, **kwargs)


@extend_schema_view(
    destroy=extend_schema(
        summary='Удалить заявку на тренерство',
        tags=['Управление заявками'],
        description='Удаление может производить только администратор или менеджер.\n'
                    'Так будет лучше т.к. человек не сможет спамить заявками\n'
                    'удаляя и создавая их по новой.'
    ),
    change_status_application=extend_schema(
        summary='Изменить статус заявки',
        tags=['Управление заявками'],
        description='Та же схема что и с другими заявками.',
    ),
)
class ApplicationManagementView(DestroyViewSet):
    queryset = Application.objects.all()

    multi_serializer_class = {
        'destroy': applications.ApplicationDestroySerializer,
        'change_status_application': applications.ApplicationChangeStatusSerializer,
    }

    permission_classes = [CanManageApplications]

    @action(
        methods=['patch'], detail=True,
    )
    def change_status_application(self, request, *args, **kwargs):
        application = Application.objects.filter(pk=kwargs.get('pk')).first()
        status = Status.objects.filter(code=request.data.get('status')).first().code

        if application and status:
            serializer = self.get_serializer(instance=application, data={'status': status})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=HTTP_204_NO_CONTENT)
        return Response(status=HTTP_400_BAD_REQUEST, data='Неправильный статус или заявка.')
