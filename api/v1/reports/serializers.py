from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.v1.reports.models import Report


class ReportSerializer(serializers.ModelSerializer):
    student = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Report
        exclude = ['created_at', 'is_completed']

    def validate(self, attrs):
        lesson = attrs['lesson']
        question = attrs['question']
        if not (lesson or question) or lesson and question:
            raise ValidationError('lesson or question is required')
        return super().validate(attrs)
