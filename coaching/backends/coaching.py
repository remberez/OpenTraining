from django.contrib.auth import get_user_model
from django.db.models import Q

from users.constants import positions
from rest_framework import filters
import django_filters

User = get_user_model()


class CoachingFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if request.user.position.code == positions.ADMIN_CODE:
            return queryset
        return queryset.filter(
            pk=request.user.pk
        )


class CoachingSearchFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='search_filter')

    class Meta:
        model = User
        fields = (
            'search',
        )

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            Q(teacher_coaching__teacher__username__icontains=value) |
            Q(teacher_coaching__learner__username__icontains=value) |
            Q(learner_coaching__learner__username__icontains=value) |
            Q(learner_coaching__teacher__username__icontains=value) |
            Q(learner_coaching__game__game__name__icontains=value) |
            Q(teacher_coaching__game__game__name__icontains=value)
        )
