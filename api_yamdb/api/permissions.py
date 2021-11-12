from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Allow access for superuser or for user with admin role."""
    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated
            and (user.role == 'admin' or user.is_superuser)
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Allow full access for superuser or for user with admin role.
    And read only access for others.
    """
    def has_permission(self, request, view):
        user = request.user
        return (
            request.method in permissions.SAFE_METHODS
            or (
                user.is_authenticated and (
                    user.role == 'admin' or user.is_superuser
                )
            )
        )
