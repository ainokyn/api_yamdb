from rest_framework import permissions, status


class AnonymModeratorAdminAuthor(permissions.BasePermission):
    message = status.HTTP_403_FORBIDDEN
    edit_methods = ("PUT", "PATCH", "DELETE",)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method in self.edit_methods:
            if request.user.role == (request.user.moderator or
                                     request.user.admin):
                return True
            if obj.author == request.user:
                return True
