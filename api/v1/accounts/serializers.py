from django.conf import settings
from rest_framework import serializers
from django.core.cache import cache

from api.v1.general.utils import get_language
from api.v1.lessons.models import Lesson
from api.v1.accounts.models import CustomUser
from api.v1.questions.models import Question


class ProfileSerializer(serializers.ModelSerializer):
    all_lessons_count = serializers.SerializerMethodField()
    all_questions_count = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'email', 'avatar_id', 'user_code', 'bonus_money', 'ball',
            'completed_lessons', 'all_lessons_count', 'all_questions_count', 'wrong_answers',
            'last_exams_result', 'level', 'level_image_id', 'tariff_expire_date'
        ]

    def get_level(self, instance):
        return settings.LEVEL_NAMES[get_language()][instance.level]

    def get_all_lessons_count(self, instance):
        cnt = cache.get('all_lessons_count')
        if not cnt:
            Lesson.set_redis()
            cnt = cache.get('all_lessons_count')

        return cnt if cnt else 0

    def get_all_questions_count(self, instance):
        cnt = cache.get('all_questions_count')
        if not cnt:
            Question.set_redis()
            cnt = cache.get('all_questions_count')

        return cnt if cnt else 0


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'avatar_id', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
