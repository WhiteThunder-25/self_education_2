from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from disciplines.models import Lesson
from users.models import User


class DisciplinesTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(email="test@test.ru")
        teachers_group = Group.objects.create(name="Teachers")
        self.user.groups.add(teachers_group)
        self.client.force_authenticate(user=self.user)
        self.lesson = Lesson.objects.create(name="Занятие 1", description="Введение в тему",
                                            video_link="https://www.youtube.com/lesson1/",
                                            owner=self.user)

    def test_lesson_detail(self):
        url = reverse("disciplines:lesson", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.lesson.name)
        self.assertEqual(self.lesson.owner, self.user)

    def test_lesson_create(self):
        url = reverse("disciplines:create_lesson")
        data = {"name": "test_lesson", "video_link": "https://www.youtube.com/testlesson/"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_create_forbidden(self):
        teachers_group = Group.objects.get(name="Teachers")
        self.user.groups.remove(teachers_group)
        url = reverse("disciplines:create_lesson")
        data = {"name": "test_lesson", "video_link": "https:///www.youtube.com/testlesson/"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Lesson.objects.all().count(), 1)

    def test_lesson_create_invalid_link(self):
        url = reverse("disciplines:create_lesson")
        data = {"name": "test_lesson", "video_link": "https://www.vkvideo.com/testlesson/"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json().get("video_link"),
                         ["Неверная ссылка на видео. Добавьте ссылку на видео с Youtube или Rutube"])
        self.assertEqual(Lesson.objects.all().count(), 1)

    def test_lesson_update(self):
        url = reverse("disciplines:update_lesson", args=(self.lesson.pk,))
        data = {"name": "test_lesson1"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "test_lesson1")

    def test_lesson_delete(self):
        url = reverse("disciplines:delete_lesson", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse("disciplines:lessons")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "name": self.lesson.name,
                    "description": self.lesson.description,
                    "topic": None,
                    "video_link": self.lesson.video_link,
                }
            ]}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
