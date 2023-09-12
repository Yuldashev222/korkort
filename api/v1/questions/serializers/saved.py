from django.conf import settings
from django.db import transaction
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

        for pk in question_ids:
            StudentSavedQuestion.objects.get_or_create(student=student, question_id=pk)
        return {}


@transaction.atomic
def delete_saved_questions(student_id, question_ids):
    for pk in question_ids:
        try:
            StudentSavedQuestion.objects.get_or_create(student_id=student_id, question_id=pk)
        except StudentSavedQuestion.DoesNotExist:
            raise ValidationError({'pk': 'not found'})


class SavedQuestionListDeleteSerializer(SavedQuestionListCreateSerializer):
    questions = serializers.ListSerializer(child=QuestionAnswerSerializer(), max_length=settings.MAX_QUESTIONS)

    def to_internal_value(self, data):
        super().to_internal_value(data)
        student = self.context['request'].user
        question_ids = list(set(question['pk'] for question in data['questions']))
        delete_saved_questions(student_id=student.id, question_ids=question_ids)
        return {}
