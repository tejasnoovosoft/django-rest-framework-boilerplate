from rest_framework.permissions import BasePermission

from user.enums import UserRole


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == UserRole.ADMIN.value
        )
