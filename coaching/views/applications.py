import datetime
from django.apps import apps
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from coaching.backends import ApplicationFilter
from coaching.models.applications import Application, Status
from coaching.permissions import CanManageApplications, IsManagerOfCurrentlyApplication
from common.views.mixins import CRDViewSet, CRUDViewSet, UDViewSet, CRViewSet, DestroyViewSet
from coaching.serializers import applications
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.filters import OrderingFilter, SearchFilter
from coaching.constants.statuses import *
from django.core.mail import send_mail
from google.apps import meet_v2
from users.constants import positions


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

    def create(self, request, *args, **kwargs):
        if self.filter_queryset(self.get_queryset()) and not IsAdminUser().has_permission(request, self):
            return Response(status=status.HTTP_403_FORBIDDEN)
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

    base_cods = {
        'waiting': WAITING_STATUS_CODE,
        'processing': PROCESSING_STATUS_CODE,
        'approved': APPROVED_STATUS_CODE,
        'accepted': ACCEPTED_STATUS_CODE,
    }

    def destroy(self, request, *args, **kwargs):
        code = kwargs.get('pk')
        if code and code in self.base_cods.values():
            return Response(status=status.HTTP_400_BAD_REQUEST, data='Невозможно удалить данный статус')
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
    take_application=extend_schema(
        summary='Взять заявку на обработку',
        tags=['Управление заявками'],
    ),
    create_google_meet=extend_schema(
        summary='Создать гугл встречу по заявке',
        tags=['Управление заявками'],
        parameters=None
    ),
    application_for_processing=extend_schema(
        summary="Отправить заявку на рассмотрение",
        tags=['Управление заявками'],
        parameters=None,
    ),
    approve_application=extend_schema(
        summary="Одобрить заявку",
        tags=['Управление заявками'],
        parameters=None,
    ),
    reject_application=extend_schema(
        summary="Отклонить заявку",
        tags=['Управление заявками'],
        parameters=None,
    )
)
class ApplicationManagementView(DestroyViewSet):
    queryset = Application.objects.all()

    multi_serializer_class = {
        'change_status_application': applications.ApplicationChangeStatusSerializer,
        'take_application': applications.TakeApplicationSerializer,
    }

    permission_classes = [IsManagerOfCurrentlyApplication | IsAdminUser]
    multi_permission_classes = {
        "change_status_application": [IsAdminUser],
        "take_application": [CanManageApplications]
    }

    @action(
        methods=['patch'], detail=True,
    )
    def change_status_application(self, request, *args, **kwargs):
        application = self.get_object()
        if application:
            serializer = self.get_serializer(instance=application, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST, data='Неправильный статус или заявка.')

    @action(
        methods=['patch'], detail=True,
    )
    def take_application(self, request, *args, **kwargs):
        application = Application.objects.filter(pk=kwargs.get('pk')).first()
        if application:
            if not application.manager:
                serializer = self.get_serializer(self.get_object(), data=self.request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(status=status.HTTP_200_OK)
            else:
                # Думал какой статус код надо отправлять и увидел этот бриллиант, поэтому тут чайник
                return Response(status=status.HTTP_418_IM_A_TEAPOT, data='Данная заявка уже обрабатывается')
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data='Заявки не существует')

    def send_message_about_call(self, data, application):
        title = f'Вы были приглашены на обзвон в дискорд по вашей заявке {application.id}'
        message = f'''
                    Здравствуйте, {application.full_name}!
                    Благодарим вас за вашу заявку на тренерство на нашем сайте! Мы рады сообщить, что ваша кандидатура
                    была успешно получена, и мы хотели бы обсудить с вами детали вашего опыта и пожеланий.
                    **Дата и время звонка:** {data['date_of_call']}.
                    Пожалуйста, убедитесь, что у вас будет возможность пообщаться в указанное время. Если по какой-либо
                    причине вы не сможете ответить на звонок или вам требуется изменить время, дайте нам знать заранее 
                    – мы постараемся учесть ваши пожелания.
                    В ожидании разговора!
                   '''

        return send_mail(
            title,
            message,
            "agasianartyom@yandex.ru",
            [application.sender.email],
            fail_silently=False
        )

    @action(
        methods=['get'], detail=True
    )
    def create_google_meet(self, request, *args, **kwargs):
        application = self.get_object()
        if not application.google_meet_uri:
            date_of_call = application.date_of_call
            delta = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30)
            if delta >= date_of_call:
                try:
                    coaching_config = apps.get_app_config('coaching')
                    client = meet_v2.SpacesServiceClient(credentials=coaching_config.creds)
                    request = meet_v2.CreateSpaceRequest()
                    response = client.create_space(request=request)
                    application.google_meet_uri = response.meeting_uri
                    application.save()
                    return Response(status=status.HTTP_200_OK, data=response.meeting_uri)
                except Exception:
                    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE, data="Встречу можно создать за 30 минут до её начала")
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="Встреча уже существует")

    @action(
        methods=['get'], detail=True
    )
    def application_for_processing(self, request, *args, **kwargs):
        self.change_application_status(PROCESSING_STATUS_CODE)
        return Response(status=status.HTTP_200_OK)

    @action(
        methods=['get'], detail=True
    )
    def approve_application(self, request, *args, **kwargs):
        self.change_application_status(APPROVED_STATUS_CODE)
        user = self.get_object().sender
        user.status = positions.TEACHER_CODE
        return Response(status=status.HTTP_200_OK)

    @action(
        methods=['get'], detail=True
    )
    def reject_application(self, request, *args, **kwargs):
        self.change_application_status(REJECTED_STATUS_CODE)
        return Response(status=status.HTTP_200_OK)

    def change_application_status(self, status_code):
        application = self.get_object()
        status_code = Status.objects.filter(code=status_code).first()
        application.status = status_code
        application.save()
