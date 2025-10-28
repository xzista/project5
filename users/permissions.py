from rest_framework.permissions import BasePermission


class UserProfilePermission(BasePermission):
    """
    Разрешение для доступа к собственному профилю.
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user