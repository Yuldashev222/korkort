from rest_framework import serializers
from django.utils.translation import get_language
from django.contrib.auth.hashers import make_password

from api.v1.exams.models import StudentLastExamResult
from api.v1.levels.models import LevelDetail
from api.v1.lessons.models import Lesson
from api.v1.accounts.models import CustomUser
from api.v1.questions.models import Question
from api.v1.exams.serializers.general import StudentLastExamResultSerializer


class ProfileSerializer(serializers.ModelSerializer):
    all_lessons_count = serializers.IntegerField(default=Lesson.get_all_lessons_count())
    all_questions_count = serializers.IntegerField(default=Question.get_all_questions_count())
    last_exams = serializers.SerializerMethodField()
    level = serializers.SerializerMethodField()

    def get_level(self, instance):
        level = {
            'id': instance.level_id,
            'percent': instance.level_percent
        }
        try:
            obj = LevelDetail.objects.get(language_id=get_language(), level__ordering_number=instance.level_id)
        except LevelDetail.DoesNotExist:
            level['name'] = '-'
        else:
            level['name'] = obj.name
        return level

    def get_last_exams(self, instance):
        last_exams = StudentLastExamResult.objects.filter(student_id=instance.pk).order_by('-pk')[:10]
        data = StudentLastExamResultSerializer(last_exams, many=True).data
        len_data = len(data)
        if len_data < 10:
            obj = {'questions': 0, 'percent': 0}
            data.extend([obj] * (10 - len_data))
        data.reverse()
        return data

    class Meta:
        model = CustomUser
        fields = [
            'name', 'ball', 'email', 'avatar_id', 'user_code', 'bonus_money', 'completed_lessons',
            'all_lessons_count', 'all_questions_count', 'correct_answers', 'tariff_expire_date', 'level', 'last_exams'
        ]


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['name', 'avatar_id', 'password']
        extra_kwargs = {'name': {'min_length': 3},
                        'password': {'write_only': True, 'style': {'input_type': 'password'}}}

    def update(self, instance, validated_data):
        if validated_data.get('password'):
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)
