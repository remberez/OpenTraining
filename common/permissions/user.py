from rest_framework.permissions import BasePermission


class IsUsersAccountOrPublic(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj or obj.is_public
