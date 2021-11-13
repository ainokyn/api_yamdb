from rest_framework import permissions, status


class AnonymModeratorAdminAuthor(permissions.BasePermission):
    message = status.HTTP_403_FORBIDDEN
    edit_methods = ("PUT", "PATCH", "DELETE",)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return (request.method in permissions.SAFE_METHODS)
        if request.method in self.edit_methods:
            if obj.author == request.user:
                return True
            return(request.user.role == 'moderator' or 'admin')


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
