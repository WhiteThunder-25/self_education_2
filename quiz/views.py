from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.permissions import IsAdmin, IsOwner, IsTeacher, IsStudent

from quiz.models import Answer, Quiz, Question
from quiz.paginators import CustomPagination
from quiz.serializers import (
    AnswerSerializer,
    QuizSerializer,
    QuestionSerializer,
)


class QuizListApiView(ListAPIView):
    """Просмотр списка тестов."""

    serializer_class = QuizSerializer
    pagination_class = CustomPagination
    queryset = Quiz.objects.all()
    permission_classes = (IsAuthenticated, IsAdmin, IsTeacher, IsStudent)


class QuizDetailApiView(RetrieveAPIView):
    """Просмотр выбранного теста."""

    serializer_class = QuizSerializer
    queryset = Quiz.objects.all()
    permission_classes = (IsAuthenticated, IsAdmin, IsTeacher, IsStudent)


class QuizCreateApiView(CreateAPIView):
    """Создание теста."""

    serializer_class = QuizSerializer
    queryset = Quiz.objects.all()
    permission_classes = (IsAuthenticated, IsTeacher)

    def perform_create(self, serializer):
        lesson = serializer.save(owner=self.request.user)
        lesson.save()

class QuizUpdateApiView(UpdateAPIView):
    """Редактирование выбранного теста."""

    serializer_class = QuizSerializer
    queryset = Quiz.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)


class QuizDeleteApiView(DestroyAPIView):
    """Удаление теста."""

    serializer_class = QuizSerializer
    queryset = Quiz.objects.all()
    permission_classes = (IsAuthenticated, IsAdmin | IsOwner)


class QuestionListApiView(ListAPIView):
    """Просмотр списка вопросов."""

    serializer_class = QuestionSerializer
    pagination_class = CustomPagination
    queryset = Question.objects.all()
    permission_classes = (IsAuthenticated, IsAdmin, IsTeacher, IsStudent)
    ordering_fields = ("pk",)


class QuestionDetailApiView(RetrieveAPIView):
    """Просмотр выбранного вопроса."""

    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    permission_classes = (IsAuthenticated, IsAdmin, IsTeacher, IsStudent)


class QuestionCreateApiView(CreateAPIView):
    """Создание вопроса."""

    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    permission_classes = (IsAuthenticated, IsTeacher)

    def perform_create(self, serializer):
        lesson = serializer.save(owner=self.request.user)
        lesson.save()

class QuestionUpdateApiView(UpdateAPIView):
    """Редактирование выбранного вопроса."""

    serializer_class = QuestionSerializer
    queryset = Quiz.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)


class QuestionDeleteApiView(DestroyAPIView):
    """Удаление выбранного вопроса."""

    serializer_class = QuestionSerializer
    queryset = Quiz.objects.all()
    permission_classes = (IsAuthenticated, IsAdmin | IsOwner)


class AnswerListApiView(ListAPIView):
    """Просмотр списка ответов."""

    serializer_class = AnswerSerializer
    pagination_class = CustomPagination
    queryset = Answer.objects.all()
    permission_classes = (IsAuthenticated, IsAdmin, IsTeacher)


class AnswerDetailApiView(RetrieveAPIView):
    """Просмотр выбранного ответа."""

    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()
    permission_classes = (IsAuthenticated, IsAdmin, IsTeacher)


class AnswerCreateApiView(CreateAPIView):
    """Создание ответа."""

    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()
    permission_classes = (IsAuthenticated, IsTeacher)

    def perform_create(self, serializer):
        lesson = serializer.save(owner=self.request.user)
        lesson.save()


class AnswerUpdateApiView(UpdateAPIView):
    """Редактирование выбранного ответа."""

    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)


class AnswerDeleteApiView(DestroyAPIView):
    """Удаление выбранного ответа."""

    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()
    permission_classes = (IsAuthenticated, IsAdmin | IsOwner)


class GetQuestions(APIView):
    """Получение вопросов для теста по id теста."""

    permission_classes = (IsAuthenticated, IsStudent)

    def get(self, request, *args, **kwargs):

        quiz = Quiz.objects.get(pk=kwargs["lesson_pk"])
        questions_list = quiz.question_set.all().values()
        return Response({"Вопросы": list(questions_list)})


class GetAnswers(APIView):
    """Получение ответов для теста по id вопроса."""

    permission_classes = (IsAuthenticated, IsStudent)

    def get(self, request, *args, **kwargs):
        question = Question.objects.get(pk=kwargs["question_pk"])
        answers_list = question.answer_set.all().values()
        return Response({"Варианты ответа": list(answers_list)})


class GetAnswers2(APIView):
    """Получение ответов для теста по id теста и id вопроса."""

    def get(self, request, *args, **kwargs):

        permission_classes = (IsAuthenticated, IsStudent)

        lesson_pk = kwargs["lesson_pk"]
        print(lesson_pk)
        question_pk = kwargs["question_pk"]
        print(question_pk)

        quiz = Quiz.objects.get(pk=lesson_pk)

        questions = quiz.question_set.filter(quiz=lesson_pk)
        question = questions.get(pk=question_pk)

        answers_list = question.answer_set.all().values()
        return Response({"Варианты ответа": list(answers_list)})


class GetIsCorrectAnswer(APIView):
    """Получение правильного ответа по id вопроса."""

    permission_classes = (IsAuthenticated, IsTeacher)

    def get(self, request, *args, **kwargs):
        question = Question.objects.get(pk=kwargs["question_pk"])
        answer_list = question.answer_set.filter(is_correct=True).values()
        return Response({"Правильный ответ": list(answer_list)})


class AnswerVerification(APIView):
    """Проверка правильности ответа по id вопроса и id ответа."""

    permission_classes = (IsAuthenticated, IsTeacher)

    def post(self, request, *args, **kwargs):
        question_pk = kwargs["question_pk"]
        answer_pk = kwargs["answer_pk"]

        question = Question.objects.get(pk=question_pk)
        answers_list = question.answer_set.filter(is_correct=True).values()
        pk_list = []

        for item in answers_list:
            pk_list.append(item["id"])
        if answer_pk in pk_list:
            message = "Верно!"
        else:
            message = "Неверно!"

        return Response({"message": message})
