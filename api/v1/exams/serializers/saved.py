from django.db import transaction
from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.v1.exams.models import StudentLastExamResult
from api.v1.questions.tasks import update_student_wrong_answers, update_student_correct_answers
from api.v1.questions.models import Question
from api.v1.exams.serializers.categories import CategoryExamAnswerSerializer


class SavedQuestionsExamAnswerSerializer(CategoryExamAnswerSerializer):
    category_id = None
    wrong_question_id_list = serializers.ListField(child=serializers.IntegerField(),
                                                   max_length=settings.MAX_QUESTIONS)
    correct_question_id_list = serializers.ListField(child=serializers.IntegerField(),
                                                     max_length=settings.MAX_QUESTIONS)

    @transaction.atomic
    def to_internal_value(self, data):
        serializers.Serializer.to_internal_value(self, data)
        student = self.context['request'].user
        wrong_question_id_list = list(set(data['wrong_question_id_list']))
        correct_question_id_list = list(set(data['correct_question_id_list']))
        correct_question_id_list = [i for i in correct_question_id_list if i not in wrong_question_id_list]

        all_question_count = len(wrong_question_id_list) + len(correct_question_id_list)
        if all_question_count > settings.MAX_QUESTIONS:
            raise ValidationError({'detail': 'max length'})

        elif all_question_count < settings.MIN_QUESTIONS:
            raise ValidationError({'detail': 'min length'})

        for question_ids in [correct_question_id_list, wrong_question_id_list]:  # last
            for pk in question_ids:
                if not Question.is_correct_question_id(question_id=pk):
                    raise ValidationError({'question_id': 'not found'})

        wrong_question_count = len(wrong_question_id_list)

        StudentLastExamResult.objects.create(wrong_answers=wrong_question_count, questions=all_question_count,
                                             student_id=student.pk)

        update_student_correct_answers(student=student, wrong_question_ids=wrong_question_id_list,
                                       correct_question_ids=correct_question_id_list)
        update_student_wrong_answers.delay(student_id=student.pk, wrong_question_ids=wrong_question_id_list,
                                           correct_question_ids=correct_question_id_list)

        return data
