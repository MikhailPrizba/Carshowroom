from rest_framework import permissions
from user.models import User


class UpdatePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if (
            request.method == "PUT"
            or request.method == "PATCH"
            and "balance" in request.data
        ):
            if (
                request.user.is_superuser
                or request.user.user_role == User.UserRoleChoices.ADMIN
            ):
                return True
            return False
        return True


class IsCustomerOrSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if (
            request.user.is_superuser
            or request.user.user_role == User.UserRoleChoices.CUSTOMER
        ):
            return True
        return False
