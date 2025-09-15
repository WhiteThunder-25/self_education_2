from django.urls import path

from quiz.apps import QuizConfig
from quiz.views import (
    AnswerCreateApiView,
    AnswerDeleteApiView,
    AnswerDetailApiView,
    AnswerListApiView,
    AnswerUpdateApiView,
    AnswerVerification,
    QuizCreateApiView,
    QuizDeleteApiView,
    QuizDetailApiView,
    QuizListApiView,
    QuizUpdateApiView,
    GetAnswers,
    GetAnswers2,
    GetIsCorrectAnswer,
    GetQuestions,
    QuestionCreateApiView,
    QuestionDeleteApiView,
    QuestionDetailApiView,
    QuestionListApiView,
    QuestionUpdateApiView,
)

app_name = QuizConfig.name

urlpatterns = [
    path("quiz/list/", QuizListApiView.as_view(), name="quiz_list"),
    path("quiz/detail/<int:pk>/", QuizDetailApiView.as_view(), name="quiz_detail"),
    path("quiz/create/", QuizCreateApiView.as_view(), name="quiz_create"),
    path("quiz/update/<int:pk>/", QuizUpdateApiView.as_view(), name="quiz_update"),
    path("quiz/delete/<int:pk>/", QuizDeleteApiView.as_view(), name="quiz_delete"),
    path("question/list/", QuestionListApiView.as_view(), name="question_list"),
    path("question/detail/<int:pk>/", QuestionDetailApiView.as_view(), name="question_detail"),
    path("question/create/", QuestionCreateApiView.as_view(), name="question_create"),
    path("question/update/<int:pk>/", QuestionUpdateApiView.as_view(), name="question_update"),
    path("question/delete/<int:pk>/", QuestionDeleteApiView.as_view(), name="question_delete"),
    path("answer/list/", AnswerListApiView.as_view(), name="answer_list"),
    path("answer/detail/<int:pk>/", AnswerDetailApiView.as_view(), name="answer_detail"),
    path("answer/create/", AnswerCreateApiView.as_view(), name="answer_create"),
    path("answer/update/<int:pk>/", AnswerUpdateApiView.as_view(), name="answer_update"),
    path("answer/delete/<int:pk>/", AnswerDeleteApiView.as_view(), name="answer_delete"),
    path("get/questions/<int:lesson_pk>/", GetQuestions.as_view(), name="get_questions"),
    path("get/answers/<int:question_pk>/", GetAnswers.as_view(), name="get_answers"),
    path("get/answers2/<int:lesson_pk>/<int:question_pk>/", GetAnswers2.as_view(), name="get_answers2"),
    path("get/is_correct_answer/<int:question_pk>/", GetIsCorrectAnswer.as_view(), name="get_is_correct_answers"),
    path("answer/verification/<int:question_pk>/<int:answer_pk>/", AnswerVerification.as_view(), name="answer_verification"),
]
