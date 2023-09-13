from django.db import IntegrityError
from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.v1.questions.models import Question, StudentSavedQuestion
from api.v1.questions.serializers.questions import QuestionAnswerSerializer


class SavedQuestionListCreateSerializer(serializers.Serializer):
    questions = serializers.ListSerializer(child=QuestionAnswerSerializer(), max_length=settings.MAX_QUESTIONS)

    def to_internal_value(self, data):
        super().to_internal_value(data)
        student = self.context['request'].user
        question_ids = list(set(question['pk'] for question in data['questions']))

        for pk in question_ids:
            if not Question.is_correct_question_id(question_id=pk):
                raise ValidationError({'pk': 'not found'})

        try:
            objs = [StudentSavedQuestion(student=student, question_id=pk) for pk in question_ids]
            StudentSavedQuestion.objects.bulk_create(objs)
        except IntegrityError:
            raise ValidationError({'questions': 'already exists'})
        return {}


class SavedQuestionListDeleteSerializer(SavedQuestionListCreateSerializer):
    questions = serializers.ListSerializer(child=QuestionAnswerSerializer(), max_length=settings.MAX_QUESTIONS)

    def to_internal_value(self, data):
        super().to_internal_value(data)
        student = self.context['request'].user
        question_ids = list(set(question['pk'] for question in data['questions']))
        StudentSavedQuestion.objects.filter(id__in=question_ids, student=student).delete()
        return {}
