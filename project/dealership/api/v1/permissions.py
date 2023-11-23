from rest_framework import permissions
from user.models import User


class UpdatePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if (
            request.user.user_role == User.UserRoleChoices.ADMIN
            and "balance" in request.data
        ):
            return True
        return False


class IsDealershipOrSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if (
            request.user.is_superuser
            or request.user.user_role == User.UserRoleChoices.DEALERSHIP
        ):
            return True
        return False
