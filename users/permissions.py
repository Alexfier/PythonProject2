# -*- coding:utf-8 -*-
from rest_framework import permissions


class IsOwnerPermission(permissions.BasePermission):
    message = "Доступ открыт только владельцев"

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsPublicPermission(permissions.BasePermission):
    message = "Владелец закрыл общий доступ к привычке"

    def has_object_permission(self, request, view, obj):
        return obj.is_public
