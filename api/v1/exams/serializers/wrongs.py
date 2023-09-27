import random

from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.v1.exams.models import StudentLastExamResult
from api.v1.general.utils import get_language
from api.v1.questions.tasks import update_student_wrong_answers, update_student_correct_answers
from api.v1.questions.models import Question
from api.v1.exams.serializers.categories import CategoryExamAnswerSerializer
from api.v1.questions.serializers.variants import VariantSerializer
from api.v1.questions.tests import gifs


class WrongQuestionsExamSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='question_id')
    category = serializers.SerializerMethodField()
    category_id = serializers.IntegerField(source='question.category_id')
    question_text = serializers.SerializerMethodField()
    # question_gif = serializers.FileField(source='question.gif')
    # question_gif = serializers.URLField(source='question.get_random_gif')
    # question_gif_last_frame_number = serializers.IntegerField(source='question.gif_last_frame_number')
    # question_gif_last_frame_number = serializers.IntegerField(source=1302)
    # question_gif_duration = serializers.FloatField(default=59220)
    question_image = serializers.ImageField(source='question.image')
    answer = serializers.CharField(source='question.answer')
    is_saved = serializers.SerializerMethodField()

    variant_set = VariantSerializer(source='question.variant_set', many=True)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['question_gif'], ret['question_gif_last_frame_number'], ret['question_gif_duration'] = random.choice(gifs)
        return ret

    def get_category(self, instance):
        return getattr(instance.question.category, 'name_' + get_language())

    def get_is_saved(self, instance):
        return Question.is_correct_question_id(question_ids=self.context['student_saved_question_ids'],
                                               question_id=instance.question.id)

    def get_question_text(self, instance):
        return getattr(instance.question, 'text_' + get_language())


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
