from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Проверка, является ли пользователь администратором."""
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Admins").exists()


class IsOwner(BasePermission):
    """Проверка, является ли пользователь владельцем."""
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsTeacher(BasePermission):
    """Проверка, является ли пользователь преподавателем."""
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Teachers").exists()


class IsStudent(BasePermission):
    """Проверка, является ли пользователь преподавателем."""
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Students").exists()
