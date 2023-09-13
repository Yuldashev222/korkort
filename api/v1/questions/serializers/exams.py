from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.v1.exams.models import CategoryExamStudent, CategoryExamStudentResult
from api.v1.questions.tasks import update_student_wrong_answers_in_exam, delete_student_correct_and_wrong_fields
from api.v1.questions.models import Question, QuestionStudentLastResult, Category, StudentWrongAnswer
from api.v1.questions.serializers.questions import QuestionSerializer, QuestionAnswerSerializer


class QuestionExamSerializer(QuestionSerializer):
    lesson = serializers.SerializerMethodField()
    answer = serializers.CharField()

    def get_lesson(self, instance):
        student = self.context['request'].user
        return instance.lesson.lessonstudent_set.get(student=student, lesson=instance.lesson).id


class QuestionExamCreateSerializer(serializers.ModelSerializer):
    obj = None
    category_id = serializers.IntegerField()
    difficulty_level = serializers.ChoiceField(choices=Question.DIFFICULTY_LEVEL, allow_null=True)

    def validate_category_id(self, cat_id):
        try:
            Category.objects.get(id=cat_id)
        except Category.DoesNotExist:
            raise ValidationError({'category_id': 'not found'})
        return cat_id

    def create(self, validated_data):
        validated_data.pop('difficulty_level')
        cat_id = validated_data.pop('category_id')
        student = self.context['request'].user
        result, _ = CategoryExamStudentResult.objects.get_or_create(category_id=cat_id, student=student)
        self.obj = CategoryExamStudent.objects.create(result=result, **validated_data)
        return self.obj

    class Meta:
        model = CategoryExamStudent
        fields = ['id', 'category_id', 'questions', 'difficulty_level']


class CategoryExamAnswerSerializer(serializers.Serializer):
    exam_id = serializers.IntegerField()
    time = serializers.FloatField(default=0)
    wrong_questions = serializers.ListSerializer(child=QuestionAnswerSerializer(), max_length=settings.MAX_QUESTIONS)
    correct_questions = serializers.ListSerializer(child=QuestionAnswerSerializer(), max_length=settings.MAX_QUESTIONS)

    def to_internal_value(self, data):
        super().to_internal_value(data)
        wrong_questions = data['wrong_questions']
        correct_questions = data['correct_questions']

        if len(wrong_questions) + len(correct_questions) > settings.MAX_QUESTIONS:
            raise ValidationError('max length')

        wrong_question_ids = list(set(question['pk'] for question in wrong_questions))
        correct_question_ids = list(set(question['pk'] for question in correct_questions))
        wrong_question_ids = [i for i in wrong_question_ids if i not in correct_question_ids]

        exam_id = data['exam_id']
        student = self.context['request'].user

        try:
            exam = CategoryExamStudent.objects.get(id=exam_id)
        except CategoryExamStudent.DoesNotExist:
            raise ValidationError({'exam_id': 'not found'})

        if exam.correct_answers > 0:
            raise ValidationError({'exam_id': 'not found'})

        for question_ids in [correct_question_ids, wrong_question_ids]:
            for pk in question_ids:
                if not Question.is_correct_question_id(question_id=pk):
                    raise ValidationError({'pk': 'not found'})

        wrong_answers_cnt = len(wrong_question_ids)
        QuestionStudentLastResult.objects.create(wrong_answers=wrong_answers_cnt, questions=exam.questions,
                                                 student=student)

        exam.correct_answers = exam.questions - wrong_answers_cnt
        exam.time = data['time']
        exam.save()
        update_student_wrong_answers_in_exam.delay(student_id=student.id, wrong_question_ids=wrong_question_ids,
                                                   correct_question_ids=correct_question_ids)

        return data


class WrongQuestionsExamAnswerSerializer(CategoryExamAnswerSerializer):
    time = None
    exam_id = None
    wrong_questions = None
    question_counts = serializers.IntegerField()

    def to_internal_value(self, data):
        serializers.Serializer.to_internal_value(self, data)
        student = self.context['request'].user
        correct_question_ids = list(set(question['pk'] for question in data['correct_questions']))
        question_counts = data['question_counts']

        for pk in correct_question_ids:
            if not Question.is_correct_question_id(question_id=pk):
                raise ValidationError({'pk': 'not found'})

        correct_answers_cnt = len(correct_question_ids)
        QuestionStudentLastResult.objects.create(wrong_answers=question_counts - correct_answers_cnt, student=student,
                                                 questions=question_counts)

        delete_student_correct_and_wrong_fields.delay(StudentWrongAnswer, correct_question_ids, student.id)
        return data
