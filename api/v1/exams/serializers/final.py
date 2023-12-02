from django.db import transaction

from api.v1.exams.models import FinalExamStudent
from api.v1.exams.serializers.categories import CategoryMixExamAnswerSerializer


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
