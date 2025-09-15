from django.db import models

from disciplines.models import Lesson


class Quiz(models.Model):
    name = models.CharField(max_length=250, verbose_name="Название теста")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name="Курс", blank=True, null=True)

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"

    def __str__(self):
        return self.name


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, verbose_name="Тест", blank=True, null=True)
    question_text = models.CharField(max_length=300, verbose_name="Текст вопроса")

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Вопрос", blank=True, null=True)
    answer_text = models.CharField(max_length=300, verbose_name="Текст ответа")
    is_correct = models.BooleanField(default=False, verbose_name="Ответ верный")

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def __str__(self):
        return f"{self.answer_text}({self.is_correct})"
