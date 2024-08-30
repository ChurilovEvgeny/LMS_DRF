from rest_framework import permissions


class IsModer(permissions.BasePermission):
    message = "Вы не являетесь модератором"

    def has_permission(self, request, view):
        return request.user.groups.filter(name='moders').exists()


class IsOwner(permissions.BasePermission):
    message = "Вы не являетесь владельцем"

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
