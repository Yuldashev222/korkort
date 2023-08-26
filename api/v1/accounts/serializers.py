from rest_framework import serializers
from django.core.cache import cache

from api.v1.lessons.models import Lesson
from api.v1.accounts.models import CustomUser
from api.v1.questions.models import ExamQuestion


class ProfileSerializer(serializers.ModelSerializer):
    all_lessons_count = serializers.SerializerMethodField()
    all_questions_count = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'email', 'avatar_id', 'user_code', 'bonus_money', 'ball',
            'completed_lessons', 'all_lessons_count', 'all_questions_count', 'correct_answers',
            'last_exams_result', 'level', 'level_image_id'
        ]

    def get_level(self, instance):
        language = self.context['request'].query_params.get('language')
        if language not in ['swe', 'en', 'easy_swe']:
            return ''
        return getattr(instance.level, 'title_' + language)

    def get_all_lessons_count(self, instance):
        cnt = cache.get('all_lessons_count')
        if not cnt:
            Lesson.set_redis()
            cnt = cache.get('all_lessons_count')

        return cnt if cnt else 0

    def get_all_questions_count(self, instance):
        cnt = cache.get('all_questions_count')
        if not cnt:
            ExamQuestion.set_redis()
            cnt = cache.get('all_questions_count')

        return cnt if cnt else 0


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'avatar_id']
