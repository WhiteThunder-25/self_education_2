from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from disciplines.models import EducationalModule, Lesson, Topic
from disciplines.paginators import LessonPagination
from disciplines.serializers import EducationalModuleSerializer, LessonSerializer, TopicSerializer
from users.permissions import IsAdmin, IsOwner, IsTeacher


class EducationalModuleViewSet(viewsets.ModelViewSet):
    serializer_class = EducationalModuleSerializer
    queryset = EducationalModule.objects.all()

    def get_permissions(self):
        if self.action in ["create", "update", "destroy"]:
            self.permission_classes = (IsAuthenticated, IsAdmin)
        else:
            self.permission_classes = (AllowAny,)

        return super().get_permissions()


class TopicViewSet(viewsets.ModelViewSet):
    serializer_class = TopicSerializer
    queryset = Topic.objects.all()

    def get_permissions(self):
        if self.action in ["create", "update", "destroy"]:
            self.permission_classes = (IsAuthenticated, IsAdmin)
        else:
            self.permission_classes = (AllowAny,)

        return super().get_permissions()


class LessonCreateView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsTeacher | IsAdmin)

    def perform_create(self, serializer):
        lesson = serializer.save(owner=self.request.user)
        lesson.save()


@method_decorator(cache_page(60 * 15), name='dispatch')
class LessonListView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = LessonPagination


class LessonDetailView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonUpdateView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsOwner)


class LessonDeleteView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsAdmin | IsOwner)
