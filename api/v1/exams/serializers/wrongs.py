from django.db import transaction
from django.conf import settings
from rest_framework import serializers
from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework.exceptions import ValidationError

from api.v1.exams.models import StudentLastExamResult
from api.v1.questions.tasks import update_student_wrong_answers, update_student_correct_answers
from api.v1.questions.models import Question
from api.v1.exams.serializers.categories import CategoryExamAnswerSerializer


class WrongQuestionsExamSerializer(serializers.Serializer):
    my_questions = serializers.BooleanField(default=False)
    difficulty_level = serializers.ChoiceField(choices=Question.DIFFICULTY_LEVEL, allow_null=True)
    counts = serializers.IntegerField(validators=[MinValueValidator(settings.MIN_QUESTIONS),
                                                  MaxValueValidator(settings.MAX_QUESTIONS)])


class WrongQuestionsExamAnswerSerializer(CategoryExamAnswerSerializer):
    category_id = None
    wrong_question_id_list = None
    all_question_count = serializers.IntegerField(min_value=settings.MIN_QUESTIONS, max_value=settings.MAX_QUESTIONS)
    correct_question_id_list = serializers.ListField(child=serializers.IntegerField(),
                                                     max_length=settings.MAX_QUESTIONS)

    @transaction.atomic
    def to_internal_value(self, data):
        serializers.Serializer.to_internal_value(self, data)
        student = self.context['request'].user
        correct_question_id_list = list(set(data['correct_question_id_list']))
        all_question_count = data['all_question_count']

        for pk in correct_question_id_list:  # last
            if not Question.is_correct_question_id(question_id=pk):
                raise ValidationError({'question_id': 'not found'})

        correct_question_count = len(correct_question_id_list)
        wrong_question_count = all_question_count - correct_question_count

        StudentLastExamResult.objects.create(wrong_answers=wrong_question_count, questions=all_question_count,
                                             student_id=student.pk)

        update_student_correct_answers(student=student, wrong_question_ids=[],
                                       correct_question_ids=correct_question_id_list)
        update_student_wrong_answers.delay(student_id=student.pk, wrong_question_ids=[],
                                           correct_question_ids=correct_question_id_list)

        return data
