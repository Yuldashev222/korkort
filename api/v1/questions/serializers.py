from rest_framework import serializers

from api.v1.questions.models import LessonVariant


class LessonVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonVariant
        fields = ['is_correct', 'text_swe', 'text_en', 'text_easy_swe']


class LessonQuestionSerializer(serializers.Serializer):
    question_text_swe = serializers.CharField(source='text_swe')
    question_text_en = serializers.CharField(source='text_en')
    question_text_easy_swe = serializers.CharField(source='text_easy_swe')
    question_video_swe = serializers.FileField(source='video_swe')
    question_video_eng = serializers.FileField(source='video_eng')
    question_video_easy_swe = serializers.FileField(source='video_easy_swe')

    lessonvariant_set = LessonVariantSerializer(many=True)
