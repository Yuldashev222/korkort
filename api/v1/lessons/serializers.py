from rest_framework import serializers

from api.v1.lessons.models import Lesson


class LessonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['title_swe', 'title_en', 'title_easy_swe', 'is_open', 'lesson_time']
