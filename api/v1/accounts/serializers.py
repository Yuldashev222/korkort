from django.conf import settings
from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from api.v1.exams.serializers.general import StudentLastExamResultSerializer
from api.v1.general.utils import get_language
from api.v1.lessons.models import Lesson
from api.v1.accounts.models import CustomUser
from api.v1.questions.models import Question


class ProfileSerializer(serializers.ModelSerializer):
    all_lessons_count = serializers.IntegerField(default=Lesson.get_all_lessons_count())
    all_questions_count = serializers.IntegerField(default=Question.get_all_questions_count())
    level = serializers.SerializerMethodField()
    last_exams = serializers.SerializerMethodField()

    def get_last_exams(self, instance):
        last_exams = instance.studentlastexamresult_set.all()[:10]
        data = StudentLastExamResultSerializer(last_exams, many=True).data
        data.reverse()
        return data

    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'email', 'avatar_id', 'user_code', 'bonus_money', 'ball',
            'completed_lessons', 'all_lessons_count', 'all_questions_count', 'correct_answers',
            'last_exams_result', 'level', 'level_image_id', 'tariff_expire_date', 'last_exams'
        ]

    def get_level(self, instance):
        return settings.LEVELS[get_language()][instance.level]


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'avatar_id', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password(self, new_password):
        hash_password = make_password(new_password)
        return hash_password
