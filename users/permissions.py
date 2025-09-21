from rest_framework import permissions

from users.models import User


class IsModer(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moders").exists()


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, User):
            return obj == request.user
        if hasattr(obj, "owner"):
            return obj.owner == request.user
        return False


class IsOwnerOrModer(permissions.BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return (
            obj == request.user
            or request.user.is_staff
            or request.user.groups.filter(name="moders").exists()
        )
