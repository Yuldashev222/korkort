from django.conf import settings
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.v1.exams.serializers.categories import CategoryExamAnswerSerializer
from api.v1.questions.tasks import update_student_wrong_answers_in_exam
from api.v1.questions.models import Question, StudentSavedQuestion, QuestionStudentLastResult
from api.v1.questions.serializers.questions import QuestionAnswerSerializer


class SavedQuestionsExamAnswerSerializer(CategoryExamAnswerSerializer):
    exam_id = None
    saved_questions = None
    wrong_questions = serializers.ListSerializer(child=QuestionAnswerSerializer(), max_length=settings.MAX_QUESTIONS)
    correct_questions = serializers.ListSerializer(child=QuestionAnswerSerializer(), max_length=settings.MAX_QUESTIONS)
    delete_saved_questions = serializers.ListSerializer(child=QuestionAnswerSerializer(),
                                                        max_length=settings.MAX_QUESTIONS)

    @transaction.atomic
    def to_internal_value(self, data):
        serializers.Serializer.to_internal_value(self, data)
        student = self.context['request'].user
        wrong_questions = data['wrong_questions']
        correct_questions = data['correct_questions']
        delete_saved_questions = data['delete_saved_questions']

        if len(wrong_questions) + len(correct_questions) > settings.MAX_QUESTIONS:
            raise ValidationError('max length')

        wrong_question_ids = list(set(question['pk'] for question in wrong_questions))
        correct_question_ids = list(set(question['pk'] for question in correct_questions))
        delete_saved_question_ids = list(set(question['pk'] for question in delete_saved_questions))

        wrong_question_ids = [i for i in wrong_question_ids if i not in correct_question_ids]

        for question_ids in [correct_question_ids, wrong_question_ids, delete_saved_question_ids]:
            for pk in question_ids:
                if not Question.is_correct_question_id(question_id=pk):
                    raise ValidationError({'pk': 'not found'})

        StudentSavedQuestion.objects.filter(id__in=delete_saved_question_ids, student=student).delete()

        wrong_answers_cnt = len(wrong_question_ids)
        all_questions_cnt = len(correct_question_ids) + wrong_answers_cnt
        QuestionStudentLastResult.objects.create(wrong_answers=wrong_answers_cnt, questions=all_questions_cnt,
                                                 student=student)

        update_student_wrong_answers_in_exam.delay(student_id=student.id, wrong_question_ids=wrong_question_ids,
                                                   correct_question_ids=correct_question_ids)

        return data
