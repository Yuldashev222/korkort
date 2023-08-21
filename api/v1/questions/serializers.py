from rest_framework import serializers

from api.v1.lessons.models import LessonWordInfo, LessonSource


class LessonQuestionSerializer(serializers.Serializer):
    question_text_swe = serializers.CharField(source='text_swe')
    question_text_en = serializers.CharField(source='text_en')
    question_text_easy_swe = serializers.CharField(source='text_easy_swe')
    question_video_swe = serializers.FileField(source='video_swe')
    question_video_eng = serializers.FileField(source='video_eng')
    question_video_easy_swe = serializers.FileField(source='video_easy_swe')

    lessonvariant_set =
