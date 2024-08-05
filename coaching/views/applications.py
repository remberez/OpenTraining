import datetime

from rest_framework.response import Response
from rest_framework.status import HTTP_403_FORBIDDEN
from coaching.backends import ApplicationFilter
from coaching.constants.statuses import WAITING_STATUS_CODE
from coaching.models.applications import Application, Status
from common.views.mixins import CRUDViewSet
from coaching.serializers.applications import ApplicationCreateSerializer
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view, extend_schema


@extend_schema_view(
    create=extend_schema(
        summary='Создать заявку на тренерство',
        tags=['Заявки на тренерство'],
    )
)
class ApplicationView(CRUDViewSet):
    queryset = Application.objects.all()
    multi_serializer_class = {
        'create': ApplicationCreateSerializer,
        'list': ApplicationCreateSerializer,
    }

    multi_permission_classes = {
        'create': [IsAuthenticated],
        'list': [IsAuthenticated],
    }

    filter_backends = [
        ApplicationFilter,
    ]

    http_method_names = ('post', 'get',)

    def perform_create(self, serializer):
        meta_data = {
            'status': Status.objects.filter(code=WAITING_STATUS_CODE).first(),
            'sender': self.request.user,
        }
        serializer.save(**meta_data)

    def create(self, request, *args, **kwargs):
        if self.get_queryset():
            return Response(status=HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)
