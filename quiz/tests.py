from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from quiz.models import Answer, Quiz, Question
from disciplines.models import Lesson
from users.models import User


class QuizTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@example.com", is_staff=True)
        self.client.force_authenticate(user=self.user)
        self.lesson = Lesson.objects.create(
            name="История Древней Греции", description="Мифы Древней Греции"
        )
        self.quiz = Quiz.objects.create(
            name="Тест по Истории Древней Греции", lesson=self.lesson
        )

    def test_quiz_retrieve(self):
        url = reverse("quiz:quiz_detail", args=(self.quiz.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.quiz.name)

    def test_quiz_create(self):
        url = reverse("quiz:quiz_create")
        data = {"name": "Тест по литературе"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            Quiz.objects.filter(name="Тест по литературе").count(), 1
        )

    def test_quiz_update(self):
        url = reverse("quiz:quiz_update", args=(self.quiz.pk,))
        data = {"name": "Тест по биологии"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Тест по биологии")

    def test_quiz_delete(self):
        url = reverse("quiz:quiz_delete", args=(self.quiz.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Quiz.objects.all().count(), 0)

    def test_quiz_list(self):
        url = reverse("quiz:quiz_list")
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.quiz.pk,
                    "name": self.quiz.name,
                    "lesson": self.lesson.pk,
                }
            ],
        }

        self.assertEqual(data, result)


class QuestionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@example.com", is_staff=True)
        self.client.force_authenticate(user=self.user)
        self.lesson = Lesson.objects.create(
            name="История Древней Греции", description="Мифы Древней Греции"
        )
        self.quiz = Quiz.objects.create(
            quiz_name="Тест по Истории Древней Греции", lesson=self.lesson
        )
        self.question = Question.objects.create(
            question_text="Кто такой Зевс?", quiz=self.quiz
        )

    def test_question_retrieve(self):
        url = reverse("quiz:question_detail", args=(self.question.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("question_text"), self.question.question_text)

    def test_question_create(self):
        url = reverse("quiz:question_create")
        data = {"question_text": "Который час?"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.filter(question_text="Кто такой Зевс?").count(), 1)

    def test_question_list(self):
        url = reverse("quiz:question_list")
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.question.pk,
                    "question_text": self.question.question_text,
                    "quiz": self.quiz.pk,
                }
            ],
        }
        self.assertEqual(data, result)


class AnswerTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@example.com", is_staff=True)
        self.client.force_authenticate(user=self.user)
        self.lesson = Lesson.objects.create(
            name="История Древней Греции", description="Мифы Древней Греции"
        )
        self.quiz = Quiz.objects.create(
            quiz_name="Тест по Истории Древней Греции", lesson=self.lesson
        )
        self.question = Question.objects.create(
            question_text="Кто такой Зевс?", quiz=self.quiz
        )
        self.answer = Answer.objects.create(
            question=self.question, answer_text="Герой", is_correct=False
        )

    def test_answer_retrieve(self):
        url = reverse("quiz:answer_detail", args=(self.answer.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("answer_text"), self.answer.answer_text)

    def test_answer_create(self):
        url = reverse("quiz:answer_create")
        data = {"answer_text": "42", "is_correct": False}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Answer.objects.filter(is_correct=False).count(), 2)

    def test_answer_update(self):
        url = reverse("quiz:answer_update", args=(self.answer.pk,))
        data = {"answer_text": "Человек"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("answer_text"), "Никогда")

    def test_answer_delete(self):
        url = reverse("quiz:answer_delete", args=(self.answer.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Answer.objects.all().count(), 0)

    def test_answer_list(self):
        url = reverse("quiz:answer_list")
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.answer.pk,
                    "answer_text": self.answer.answer_text,
                    "is_correct": False,
                    "question": self.question.pk,
                }
            ],
        }
        self.assertEqual(data, result)
