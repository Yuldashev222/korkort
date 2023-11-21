from django.db import transaction
from django.conf import settings
from rest_framework import serializers
from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError

from api.v1.exams.models import CategoryExamStudent, CategoryExamStudentResult, StudentLastExamResult, FinalExamStudent
from api.v1.exams.serializers.categories import CategoryMixExamAnswerSerializer
from api.v1.general.utils import bubble_search
from api.v1.questions.tasks import update_student_wrong_answers, update_student_correct_answers
from api.v1.questions.models import Question, Category


class FinalExamAnswerSerializer(CategoryMixExamAnswerSerializer):
    @transaction.atomic
    def to_internal_value(self, data):
        student = self.context['request'].user
        wrong_question_id_list = list(set(data['wrong_question_id_list']))
        correct_question_id_list = list(set(data['correct_question_id_list']))
        correct_question_id_list = [i for i in correct_question_id_list if i not in wrong_question_id_list]
        all_question_count = len(wrong_question_id_list) + len(correct_question_id_list)
        correct_question_count = len(correct_question_id_list)

        data = super().to_internal_value(data)
        FinalExamStudent.objects.create(questions=all_question_count, correct_answers=correct_question_count,
                                        student_id=student.pk)
        FinalExamStudent.objects.filter(
            id__in=FinalExamStudent.objects.order_by('-id')[10:].values_list('id', flat=True)).delete()
        return data
