from django.db import transaction, IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.v1.exams.serializers.categories import CategoryExamAnswerSerializer
from api.v1.general.utils import get_language
from api.v1.questions.models import StudentSavedQuestion, Question, QuestionStudentLastResult, StudentWrongAnswer
from api.v1.questions.serializers.variants import VariantSerializer


class WrongQuestionsExamSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='question_id')
    category = serializers.StringRelatedField(source='question.category')
    category_id = serializers.IntegerField(source='question.category_id')
    question_text = serializers.SerializerMethodField()
    question_video = serializers.FileField(source='question.video')
    question_image = serializers.ImageField(source='question.image')
    lesson_id = serializers.IntegerField(source='question.lesson_id')
    answer = serializers.CharField(source='question.answer')
    is_saved = serializers.SerializerMethodField()  # last

    variant_set = VariantSerializer(source='question.variant_set', many=True)

    def get_is_saved(self, instance):
        if Question.is_correct_question_id(question_ids=self.context['student_saved_question_ids'],
                                           question_id=instance.id):
            return True
        return False

    def get_question_text(self, instance):
        return getattr(instance.question, 'text_' + get_language())


class WrongQuestionsExamAnswerSerializer(CategoryExamAnswerSerializer):
    question_counts = serializers.IntegerField()
    exam_id = None
    wrong_questions = None

    @transaction.atomic
    def to_internal_value(self, data):
        serializers.Serializer.to_internal_value(self, data)
        student = self.context['request'].user
        saved_questions = data['saved_questions']
        delete_saved_questions = data['delete_saved_questions']
        correct_questions = data['correct_questions']
        question_counts = data['question_counts']

        saved_question_ids = list(set(question['pk'] for question in saved_questions))
        correct_question_ids = list(set(question['pk'] for question in correct_questions))
        delete_saved_question_ids = list(set(question['pk'] for question in delete_saved_questions))

        delete_saved_question_ids = [i for i in delete_saved_question_ids if i not in saved_question_ids]

        for question_ids in [correct_question_ids, saved_question_ids, delete_saved_question_ids]:
            for pk in question_ids:
                if not Question.is_correct_question_id(question_id=pk):
                    raise ValidationError({'pk': 'not found'})

        try:
            objs = [StudentSavedQuestion(student=student, question_id=pk) for pk in saved_question_ids]
            StudentSavedQuestion.objects.bulk_create(objs)
        except IntegrityError:
            raise ValidationError({'saved_questions': 'already exists'})

        StudentSavedQuestion.objects.filter(id__in=delete_saved_question_ids, student=student).delete()

        wrong_answers_cnt = question_counts - len(correct_question_ids)
        QuestionStudentLastResult.objects.create(wrong_answers=wrong_answers_cnt, questions=question_counts,
                                                 student=student)

        StudentWrongAnswer.objects.filter(id__in=correct_question_ids, student=student).delete()

        return data
