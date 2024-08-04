from rest_framework.permissions import BasePermission


class IsUserAccount(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.position.code == 'admin'
