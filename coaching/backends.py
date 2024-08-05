from rest_framework.filters import SearchFilter, BaseFilterBackend
from coaching.models.applications import Application
from coaching.permissions import CanManageApplications


class CustomSearchFilter(SearchFilter):
    def get_search_terms(self, request):
        if request.query_params.get('genre'):
            return [request.query_params.get('genre')]
        return super().get_search_terms(request)

    def get_search_fields(self, view, request):
        if request.query_params.get('genre'):
            return ['genre__name']
        return super().get_search_fields(view, request)


class ApplicationFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        has_permission = CanManageApplications().has_permission(request, view)
        if not has_permission:
            return Application.objects.filter(
                sender=request.user,
            )
        return queryset
