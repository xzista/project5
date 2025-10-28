from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Только владелец может редактировать/удалять объект. Чтение для всех (по умолчанию).
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return getattr(obj, "owner", None) == request.user
