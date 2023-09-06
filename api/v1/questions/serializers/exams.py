from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.v1.balls.models import TestBall
from api.v1.exams.models import CategoryExamStudent
from api.v1.lessons.models import LessonStudent
from api.v1.questions.tasks import update_student_wrong_answers_in_exam_test
from api.v1.questions.models import Question, QuestionStudentLastResult
from api.v1.questions.serializers.questions import QuestionSerializer, QuestionAnswerSerializer


class QuestionExamSerializer(QuestionSerializer):
    lesson = serializers.SerializerMethodField()
    answer = serializers.CharField()

    def get_lesson(self, instance):
        student = self.context['request'].user
        return LessonStudent.objects.get(student=student, lesson=instance.lesson).id  # last


class QuestionExamCreateSerializer(serializers.ModelSerializer):
    student = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = CategoryExamStudent
        fields = ['id', 'student', 'category', 'time', 'questions', 'difficulty_level']


class CategoryExamAnswerSerializer(serializers.Serializer):
    exam_id = serializers.IntegerField()
    wrong_questions = serializers.ListSerializer(child=QuestionAnswerSerializer(), max_length=settings.MAX_QUESTIONS)
    correct_questions = serializers.ListSerializer(child=QuestionAnswerSerializer(), max_length=settings.MAX_QUESTIONS)

    def to_internal_value(self, data):
        super().to_internal_value(data)
        wrong_questions = data['wrong_questions']
        correct_questions = data['correct_questions']
        if len(wrong_questions) + len(correct_questions) > settings.MAX_QUESTIONS:
            raise ValidationError('max length')

        exam_id = data['exam_id']
        student = self.context['request'].user

        try:
            exam = CategoryExamStudent.objects.get(id=exam_id)
        except CategoryExamStudent.DoesNotExist:
            raise ValidationError({'exam_id': 'not found'})

        if exam.correct_answers > 0:
            raise ValidationError({'exam_id': 'not found'})

        wrong_question_ids = set(question['pk'] for question in wrong_questions)
        correct_question_ids = set(question['pk'] for question in correct_questions)

        for question_ids in [correct_question_ids, wrong_question_ids]:
            for pk in question_ids:  # last
                try:
                    Question.objects.get(pk=pk)
                except Question.DoesNotExist:
                    raise ValidationError({'pk': 'not found'})

        test_ball = TestBall.get_ball()

        if not test_ball:
            return {}

        wrong_answers_cnt = len(wrong_question_ids)
        QuestionStudentLastResult.objects.create(wrong_answers=wrong_answers_cnt, questions=exam.questions,
                                                 student=student)

        exam.correct_answers = exam.questions - wrong_answers_cnt
        exam.save()

        update_student_wrong_answers_in_exam_test.delay(student=student.id, wrong_question_ids=wrong_question_ids,
                                                        correct_question_ids=correct_question_ids)

        return data
