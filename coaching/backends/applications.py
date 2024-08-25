from rest_framework.filters import BaseFilterBackend
from coaching.models.applications import Application
from coaching.permissions import CanManageApplications


class ApplicationFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        has_permission = CanManageApplications().has_permission(request, view)
        if not has_permission:
            return Application.objects.filter(
                sender=request.user,
            )
        return queryset
