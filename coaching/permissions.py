from rest_framework.permissions import BasePermission
from users.constants import positions


class CanManageApplications(BasePermission):
    positions = (
        positions.MANAGER_CODE,
        positions.ADMIN_CODE,
    )

    def has_permission(self, request, view):
        return request.user.position.code in self.positions


class IsManagerOfCurrentlyApplication(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.manager
