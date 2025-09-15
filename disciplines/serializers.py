from rest_framework import serializers

from disciplines.models import EducationalModule, Lesson, Topic
from disciplines.validators import validate_video_link


class LessonSerializer(serializers.ModelSerializer):

    video_link = serializers.CharField(validators=[validate_video_link])

    class Meta:
        model = Lesson
        fields = ["id", "name", "description", "topic", "video_link"]


class TopicSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField(read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    class Meta:
        model = Topic
        fields = ["id", "name", "description", "educational_module", "lessons_count", "lessons"]


class EducationalModuleSerializer(serializers.ModelSerializer):
    topics_count = serializers.SerializerMethodField(read_only=True)
    topics = TopicSerializer(many=True, read_only=True)

    def get_topics_count(self, obj):
        return obj.topics.count()

    class Meta:
        model = EducationalModule
        fields = ["id", "name", "description", "topics_count", "topics"]
