from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from coaching.backends import ApplicationFilter
from coaching.constants.statuses import WAITING_STATUS_CODE
from coaching.models.applications import Application, Status
from coaching.permissions import CanManageApplications
from common.views.mixins import CRDViewSet
from coaching.serializers import applications
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.filters import OrderingFilter, SearchFilter


@extend_schema_view(
    create=extend_schema(
        summary='Создать заявку на тренерство',
        tags=['Заявки на тренерство'],
        description='Заявку на тренерство может создавать кто угодно,'
                    'но может быть только одна активная заявка'
    ),
    list=extend_schema(
        summary='Все заявки на тренерство',
        tags=['Заявки на тренерство'],
        description='Администратор или менеджер могут смотреть все заявки,'
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
        description='Удаление может производить только администратор или менеджер.'
                    'Так будет лучше т.к. человек не сможет спамить заявками'
                    'удаляя и создавая их по новой.'
    ),
    change_status_application=extend_schema(
        summary='Изменить статус заявки',
        tags=['Заявки на тренерство'],
        description='Та же схема что и с другими заявками.',
    ),
)
class ApplicationView(CRDViewSet):
    queryset = Application.objects.all()
    http_method_names = ('post', 'get', 'delete', 'patch')

    multi_serializer_class = {
        'create': applications.ApplicationCreateSerializer,
        'list': applications.ApplicationCreateSerializer,
        'retrieve': applications.ApplicationRetrieveSerializer,
        'destroy': applications.ApplicationDestroySerializer,
        'change_status_application': applications.ApplicationChangeStatusSerializer,
    }

    multi_permission_classes = {
        'create': [IsAuthenticated],
        'list': [IsAuthenticated],
        'retrieve': [IsAuthenticated],
        'destroy': [CanManageApplications],
        'change_status_application': [CanManageApplications],
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
        meta_data = {
            'status': Status.objects.filter(code=WAITING_STATUS_CODE).first(),
            'sender': self.request.user,
        }
        serializer.save(**meta_data)

    def create(self, request, *args, **kwargs):
        if self.filter_queryset(self.get_queryset()):
            return Response(status=HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

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
