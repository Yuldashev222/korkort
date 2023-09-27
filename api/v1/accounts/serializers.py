from django.conf import settings
from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from api.v1.general.utils import get_language
from api.v1.lessons.models import Lesson
from api.v1.accounts.models import CustomUser
from api.v1.questions.models import Question
from api.v1.exams.serializers.general import StudentLastExamResultSerializer


class ProfileSerializer(serializers.ModelSerializer):
    gt_correct_count = 0
    last_exams_result = 0
    all_lessons_count = serializers.IntegerField(default=Lesson.get_all_lessons_count())
    all_questions_count = serializers.IntegerField(default=Question.get_all_questions_count())
    level = serializers.SerializerMethodField()
    last_exams = serializers.SerializerMethodField()

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['level_percent'] = int(ret['correct_answers'] / self.gt_correct_count * 100)
        ret['level_id'] = settings.LEVEL_NAMES[get_language()].index(ret['level'])
        ret['last_exams_result'] = self.last_exams_result
        return ret

    def get_level(self, instance):
        level, self.gt_correct_count = instance.get_level_and_gt_correct_count(language=get_language())
        return level

    def get_last_exams(self, instance):
        last_exams = instance.studentlastexamresult_set.all()[:10]
        data = StudentLastExamResultSerializer(last_exams, many=True).data
        len_data = len(data)
        if len_data < 10:
            obj = {'questions': 0, 'percent': 0}
            data.extend([obj] * (10 - len_data))
        data.reverse()
        temp = list(map(lambda el: el['percent'], data))
        self.last_exams_result = int(sum(temp) / len(temp))
        return data

    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'email', 'avatar_id', 'user_code', 'bonus_money', 'ball',
            'completed_lessons', 'all_lessons_count', 'all_questions_count', 'correct_answers',
            'level', 'tariff_expire_date', 'last_exams'
        ]


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'avatar_id', 'password']
        extra_kwargs = {'first_name': {'min_length': 3},
                        'last_name': {'min_length': 3},
                        'password': {'write_only': True, 'style': {'input_type': 'password'}}}

    def update(self, instance, validated_data):
        if validated_data.get('password'):
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)
