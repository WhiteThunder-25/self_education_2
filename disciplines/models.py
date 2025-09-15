from django.db import models

from users.models import User


class EducationalModule(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название образовательного модуля",
                            help_text="Введите название модуля")
    description = models.TextField(verbose_name="Описание образовательного модуля", null=True, blank=True,
                                   help_text="Введите описание модуля")

    class Meta:
        verbose_name = "Образовательный модуль"
        verbose_name_plural = "Образовательные модули"

    def __str__(self):
        return self.name


class Topic(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название темы", help_text="Введите название темы")
    description = models.TextField(verbose_name="Описание темы", help_text="Введите описание темы", null=True,
                                   blank=True)
    educational_module = models.ForeignKey(EducationalModule, on_delete=models.CASCADE, help_text="Выберите модуль",
                                           verbose_name="Образовательный модуль", related_name="topics", null=True,
                                           blank=True)

    class Meta:
        verbose_name = "Образовательная тема"
        verbose_name_plural = "Образовательные темы"

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название урока", help_text="Введите название урока")
    description = models.TextField(verbose_name="Описание урока", help_text="Введите описание урока", null=True,
                                   blank=True)
    video_link = models.URLField(max_length=200, verbose_name="Ссылка на урок", help_text="Добавьте ссылку на урок")
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, verbose_name="Тема",
                              help_text="Выберите образовательную тему", related_name="lessons", null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Автор урока",
                              help_text="Выберите автора урока", related_name="lessons", null=True, blank=True)

    class Meta:
        verbose_name = "Занятие"
        verbose_name_plural = "Занятие"

    def __str__(self):
        return self.name
