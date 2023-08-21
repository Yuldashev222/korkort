from rest_framework import serializers

from api.v1.lessons.models import Lesson, LessonWordInfo, LessonSource


class LessonListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title_swe = serializers.CharField(source='lesson.title_swe')
    title_en = serializers.CharField(source='lesson.title_en')
    title_easy_swe = serializers.CharField(source='lesson.title_easy_swe')
    is_open = serializers.BooleanField(source='lesson.is_open')
    is_completed = serializers.BooleanField()
    lesson_time = serializers.IntegerField(source='lesson.lesson_time')


class LessonRetrieveSerializer(LessonListSerializer):
    image = serializers.FileField(source='lesson.image')
    text_swe = serializers.CharField(source='lesson.text_swe')
    text_en = serializers.CharField(source='lesson.text_en')
    text_easy_swe = serializers.CharField(source='lesson.text_easy_swe')
    video_swe = serializers.FileField(source='lesson.video_swe')
    video_en = serializers.FileField(source='lesson.video_en')
    video_easy_swe = serializers.FileField(source='lesson.video_easy_swe')


class LessonWordInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonWordInfo
        fields = ['id', 'text', 'info']


class LessonSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonSource
        fields = ['id', 'text', 'link']
