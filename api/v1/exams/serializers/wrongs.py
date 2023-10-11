from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.v1.exams.models import StudentLastExamResult
from api.v1.questions.tasks import update_student_wrong_answers, update_student_correct_answers
from api.v1.questions.models import Question
from api.v1.exams.serializers.categories import CategoryExamAnswerSerializer


class WrongQuestionsExamAnswerSerializer(CategoryExamAnswerSerializer):
    question_counts = serializers.IntegerField(min_value=5)
    exam_id = None
    wrong_questions = None

    @transaction.atomic
    def to_internal_value(self, data):
        serializers.Serializer.to_internal_value(self, data)
        student = self.context['request'].user
        correct_questions = data['correct_questions']
        question_counts = data['question_counts']

        correct_question_ids = list(set(question['pk'] for question in correct_questions))

        for pk in correct_question_ids:
            if not Question.is_correct_question_id(question_id=pk):
                raise ValidationError({'pk': 'not found'})

        wrong_answers_cnt = question_counts - len(correct_question_ids)
        StudentLastExamResult.objects.create(wrong_answers=wrong_answers_cnt, questions=question_counts,
                                             student=student)

        update_student_correct_answers(student=student, correct_question_ids=correct_question_ids,
                                       wrong_question_ids=[])

        update_student_wrong_answers.delay(student_id=student.id, correct_question_ids=correct_question_ids,
                                           wrong_question_ids=[])
        return data
