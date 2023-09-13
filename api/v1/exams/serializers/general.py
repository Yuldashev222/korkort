from rest_framework import serializers

from api.v1.questions.serializers.questions import QuestionSerializer


class QuestionExamSerializer(QuestionSerializer):
    lesson_id = serializers.IntegerField()
    answer = serializers.CharField()
