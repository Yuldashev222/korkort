from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.v1.exams.models import StudentLastExamResult
from api.v1.general.utils import get_language
from api.v1.questions.models import Question, StudentWrongAnswer
from api.v1.exams.serializers.categories import CategoryExamAnswerSerializer
from api.v1.questions.serializers.variants import VariantSerializer


class WrongQuestionsExamSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='question_id')
    category = serializers.SerializerMethodField()
    category_id = serializers.IntegerField(source='question.category_id')
    question_text = serializers.SerializerMethodField()
    # question_gif = serializers.FileField(source='question.gif')
    question_gif = serializers.URLField(
        default='https://www.wired.com/wp-content/uploads/2016/05/11xHTywJSoZIMTgyfgFLBJQ-1.gif')
    # question_gif_last_frame_number = serializers.IntegerField(source='question.gif_last_frame_number')
    question_gif_last_frame_number = serializers.IntegerField(default=29)
    question_gif_duration = serializers.FloatField(default=800)
    question_image = serializers.ImageField(source='question.image')
    answer = serializers.CharField(source='question.answer')
    is_saved = serializers.SerializerMethodField()  # last

    variant_set = VariantSerializer(source='question.variant_set', many=True)

    def get_category(self, instance):
        return getattr(instance.question.category, 'name_' + get_language())

    def get_is_saved(self, instance):
        if Question.is_correct_question_id(question_ids=self.context['student_saved_question_ids'],
                                           question_id=instance.id):
            return True
        return False

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

        StudentWrongAnswer.objects.filter(id__in=correct_question_ids, student=student).delete()

        return data
