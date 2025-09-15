from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny
from users.permissions import IsAdmin

from users.models import User
from users.paginators import CustomPagination
from users.serializers import UserSerializer


class UserCreateAPIView(CreateAPIView):
    """Создание пользователя."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListApiView(ListAPIView):
    """Просмотр списка пользователей."""

    serializer_class = UserSerializer
    pagination_class = CustomPagination
    queryset = User.objects.all()
    permission_classes = (IsAdmin,)
    filterset_fields = ("is_superuser",)


class UserDetailApiView(RetrieveAPIView):
    """Просмотр выбранного пользователя."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAdmin,)


class UserUpdateApiView(UpdateAPIView):
    """Редактирование пользователя."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAdmin,)


class UserDeleteApiView(DestroyAPIView):
    """Удаление пользователя."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsAdmin,)
