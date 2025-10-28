from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import User
from users.permissions import UserProfilePermission
from users.serializers import UserSerializer, UserPublicSerializer


class UserCreateAPIView(CreateAPIView):
    """Регистрация пользователя"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListApiView(ListAPIView):
    """Список всех пользователей (для администратора или менеджера)"""
    queryset = User.objects.all()
    serializer_class = UserPublicSerializer
    permission_classes = (IsAuthenticated,)


class UserRetrieveApiView(RetrieveAPIView):
    """Просмотр профиля пользователя"""
    queryset = User.objects.all()
    permission_classes = (UserProfilePermission,)

    def get_serializer_class(self):
        user = self.get_object()
        if user == self.request.user:
            return UserSerializer
        return UserPublicSerializer


class UserUpdateApiView(UpdateAPIView):
    """Редактирование профиля"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserProfilePermission,)


class UserDestroyApiView(DestroyAPIView):
    """Удаление пользователя"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserProfilePermission,)