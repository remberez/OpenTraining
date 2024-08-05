from django.contrib.auth import get_user_model
from django_filters import FilterSet, BooleanFilter

User = get_user_model()


class UserFilter(FilterSet):
    # Просто по приколу, вряд ли оно надо, когда есть view для учителей
    is_teacher = BooleanFilter(field_name='is_teacher', label='is teacher')
    is_public = BooleanFilter(field_name='is_public', label='is public')

    class Meta:
        model = User
        fields = (
            'is_teacher',
            'is_public',
        )
