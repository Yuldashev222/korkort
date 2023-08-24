from rest_framework import serializers
from django.core.cache import cache

from api.v1.lessons.models import Lesson
from api.v1.accounts.models import CustomUser


class ProfileSerializer(serializers.ModelSerializer):
    all_lesson_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'email', 'avatar_id', 'user_code', 'bonus_money', 'ball',
            'completed_lessons', 'all_lesson_count'
        ]

    def get_all_lesson_count(self, instance):
        cnt = cache.get('all_lesson_count')
        if not cnt:
            Lesson.set_redis()
            cnt = cache.get('all_lesson_count')

        return cnt if cnt else 0


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'avatar_id']
