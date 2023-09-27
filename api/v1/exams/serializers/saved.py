from django.db import transaction
from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.v1.exams.models import StudentLastExamResult
from api.v1.questions.tasks import update_student_wrong_answers, update_student_correct_answers
from api.v1.questions.models import Question
from api.v1.questions.serializers.questions import QuestionAnswerSerializer
from api.v1.exams.serializers.categories import CategoryExamAnswerSerializer


class SavedQuestionsExamAnswerSerializer(CategoryExamAnswerSerializer):
    exam_id = None
    wrong_questions = serializers.ListSerializer(child=QuestionAnswerSerializer(), max_length=settings.MAX_QUESTIONS)
    correct_questions = serializers.ListSerializer(child=QuestionAnswerSerializer(), max_length=settings.MAX_QUESTIONS)

    @transaction.atomic
    def to_internal_value(self, data):
        serializers.Serializer.to_internal_value(self, data)
        student = self.context['request'].user
        wrong_questions = data['wrong_questions']
        correct_questions = data['correct_questions']

        if len(wrong_questions) + len(correct_questions) > settings.MAX_QUESTIONS:
            raise ValidationError({'detail': 'max length'})

        if len(wrong_questions) + len(correct_questions) < 1:
            raise ValidationError({'detail': 'min length'})

        wrong_question_ids = list(set(question['pk'] for question in wrong_questions))
        correct_question_ids = list(set(question['pk'] for question in correct_questions))

        wrong_question_ids = [i for i in wrong_question_ids if i not in correct_question_ids]

        for question_ids in [correct_question_ids, wrong_question_ids]:
            for pk in question_ids:
                if not Question.is_correct_question_id(question_id=pk):
                    raise ValidationError({'pk': 'not found'})

        wrong_answers_cnt = len(wrong_question_ids)
        all_questions_cnt = len(correct_question_ids) + wrong_answers_cnt
        StudentLastExamResult.objects.create(wrong_answers=wrong_answers_cnt, questions=all_questions_cnt,
                                             student=student)

        update_student_correct_answers(student=student, wrong_question_ids=wrong_question_ids,
                                       correct_question_ids=correct_question_ids)
        update_student_wrong_answers.delay(student_id=student.id, wrong_question_ids=wrong_question_ids,
                                           correct_question_ids=correct_question_ids)

        return data
