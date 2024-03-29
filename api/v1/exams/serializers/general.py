from rest_framework import serializers

from api.v1.exams.models import StudentLastExamResult


class StudentLastExamResultSerializer(serializers.ModelSerializer):
    percent = serializers.SerializerMethodField()

    def get_percent(self, instance):
        return int((instance.questions - instance.wrong_answers) / instance.questions * 100)

    class Meta:
        model = StudentLastExamResult
        fields = ['questions', 'percent']
