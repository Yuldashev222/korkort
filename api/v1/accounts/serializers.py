from django.conf import settings
from rest_framework import serializers
from django.utils.timezone import now
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError

from api.v1.exams.models import StudentLastExamResult
from api.v1.accounts.models import CustomUser
from api.v1.questions.models import Question
from api.v1.exams.serializers.general import StudentLastExamResultSerializer


class ProfileMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'avatar_id']


class ProfileChapterSerializer(serializers.ModelSerializer):
    tariff_expire_days = serializers.SerializerMethodField()

    def get_tariff_expire_days(self, obj):
        return (now().date() - obj.tariff_expire_date).days

    class Meta:
        model = CustomUser
        fields = ['name', 'avatar_id', 'level_id', 'ball', 'user_code', 'tariff_expire_days', 'bonus_money']


class ProfileExamSerializer(ProfileChapterSerializer):
    all_questions_count = serializers.SerializerMethodField()
    last_exams = serializers.SerializerMethodField()

    def get_all_questions_count(self, obj):
        return Question.get_all_questions_count()

    def get_last_exams(self, instance):
        last_exams = StudentLastExamResult.objects.filter(student_id=instance.pk).order_by('-pk')[:10]
        data = StudentLastExamResultSerializer(last_exams, many=True).data
        len_data = len(data)
        if len_data < 10:
            obj = {'questions': 0, 'percent': 0}
            data.extend([obj] * (10 - len_data))
        data.reverse()
        return data

    class Meta(ProfileChapterSerializer.Meta):
        fields = ProfileChapterSerializer.Meta.fields + ['all_questions_count', 'correct_answers', 'last_exams']


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['name', 'avatar_id', 'password']
        extra_kwargs = {
            'name': {
                'min_length': 3
            },
            'password': {
                'write_only': True,
                'trim_whitespace': False,
                'style': {'input_type': 'password'}
            }
        }

    def validate_avatar_id(self, value):
        if not value:
            raise ValidationError()
        return value

    def update(self, instance, validated_data):
        password = validated_data.get('password')
        if password is not None:
            validated_data['password'] = make_password(password)
        return super().update(instance, validated_data)
