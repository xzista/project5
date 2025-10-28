from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter , OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from habits.models import Habit
from habits.pagination import HabitPagination
from habits.permissions import IsOwnerOrReadOnly
from habits.serializers import HabitSerializer


class HabitViewSet(ModelViewSet):
    """
    Основной ViewSet:
    - /habits/ — список привычек текущего пользователя
    - /habits/public/ — публичные привычки
    - /habits/{id}/ — детали, редактирование, удаление
    """

    serializer_class = HabitSerializer
    pagination_class = HabitPagination
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["action", "place"]
    ordering_fields = ["time", "created_at"]

    def get_queryset(self):
        """
        Возвращает привычки только текущего пользователя,
        либо публичные, если запрошен эндпоинт /public/.
        """
        if self.action == "public":
            return Habit.objects.filter(is_public=True)
        return Habit.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """
        Присваиваем текущего пользователя как владельца
        """
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=["get"], url_path="public", permission_classes=[AllowAny])
    def public(self, request):
        """
        Эндпоинт /habits/public/
        Список публичных привычек (доступен всем, read-only)
        """
        habits = Habit.objects.filter(is_public=True)
        page = self.paginate_queryset(habits)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(habits, many=True)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        """Только владелец может удалить"""
        if instance.owner != self.request.user:
            raise PermissionDenied("Вы не можете удалить чужую привычку.")
        instance.delete()
