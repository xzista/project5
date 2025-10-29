from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .apps import UsersConfig
from .views import (UserCreateAPIView, UserDestroyApiView, UserListApiView,
                    UserRetrieveApiView, UserUpdateApiView)

app_name = UsersConfig.name

urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("list/", UserListApiView.as_view(), name="user-list"),
    path("<int:pk>/", UserRetrieveApiView.as_view(), name="user-detail"),
    path("<int:pk>/update/", UserUpdateApiView.as_view(), name="user-update"),
    path("<int:pk>/delete/", UserDestroyApiView.as_view(), name="user-delete"),
]
