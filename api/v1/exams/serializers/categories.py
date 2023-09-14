from django.conf import settings
from django.db import transaction, IntegrityError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.v1.exams.models import CategoryExamStudent, CategoryExamStudentResult, StudentLastExamResult
from api.v1.general.utils import get_language
from api.v1.questions.models import Question, StudentSavedQuestion, Category
from api.v1.questions.tasks import update_student_wrong_answers_in_exam
from api.v1.questions.serializers.questions import QuestionAnswerSerializer


class CategoryExamStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryExamStudent
        fields = ['questions', 'percent']


class CategoryExamStudentResultSerializer(serializers.ModelSerializer):
    # image = serializers.SerializerMethodField()
    image = serializers.URLField(
        default='https://www.e-report.uz/media/chapters/1%3A%202014e1e9-a989-4995-b36f-77a/images/IMG.png')
    name = serializers.SerializerMethodField()
    detail = CategoryExamStudentSerializer(source='categoryexamstudent_set', many=True)

    class Meta:
        model = CategoryExamStudentResult
        exclude = ['student']

    def get_name(self, instance):
        return getattr(instance.category, 'name_' + get_language())

    # def get_image(self, instance):
    #     return self.context['request'].build_absolute_uri(instance.category.image.url)


class CategoryExamAnswerSerializer(serializers.Serializer):
    exam_id = serializers.IntegerField()
    wrong_questions = serializers.ListSerializer(child=QuestionAnswerSerializer(), max_length=settings.MAX_QUESTIONS)
    correct_questions = serializers.ListSerializer(child=QuestionAnswerSerializer(), max_length=settings.MAX_QUESTIONS)
    saved_questions = serializers.ListSerializer(child=QuestionAnswerSerializer(), max_length=settings.MAX_QUESTIONS)
    delete_saved_questions = serializers.ListSerializer(child=QuestionAnswerSerializer(),
                                                        max_length=settings.MAX_QUESTIONS)

    @transaction.atomic
    def to_internal_value(self, data):
        super().to_internal_value(data)
        student = self.context['request'].user
        exam_id = data['exam_id']
        saved_questions = data['saved_questions']
        wrong_questions = data['wrong_questions']
        correct_questions = data['correct_questions']
        delete_saved_questions = data['delete_saved_questions']

        if len(wrong_questions) + len(correct_questions) > settings.MAX_QUESTIONS:
            raise ValidationError('max length')

        try:
            exam = CategoryExamStudent.objects.get(id=exam_id)
        except CategoryExamStudent.DoesNotExist:
            raise ValidationError({'exam_id': 'not found'})

        if exam.correct_answers > 0:
            raise ValidationError({'exam_id': 'not found'})

        saved_question_ids = list(set(question['pk'] for question in saved_questions))
        wrong_question_ids = list(set(question['pk'] for question in wrong_questions))
        correct_question_ids = list(set(question['pk'] for question in correct_questions))
        delete_saved_question_ids = list(set(question['pk'] for question in delete_saved_questions))

        wrong_question_ids = [i for i in wrong_question_ids if i not in correct_question_ids]
        delete_saved_question_ids = [i for i in delete_saved_question_ids if i not in saved_question_ids]

        for question_ids in [correct_question_ids, wrong_question_ids, saved_question_ids, delete_saved_question_ids]:
            for pk in question_ids:
                if not Question.is_correct_question_id(question_id=pk):
                    raise ValidationError({'pk': 'not found'})

        try:
            objs = [StudentSavedQuestion(student=student, question_id=pk) for pk in saved_question_ids]
            StudentSavedQuestion.objects.bulk_create(objs)
        except IntegrityError:
            raise ValidationError({'saved_questions': 'already exists'})

        StudentSavedQuestion.objects.filter(id__in=delete_saved_question_ids, student=student).delete()

        wrong_answers_cnt = len(wrong_question_ids)
        StudentLastExamResult.objects.create(wrong_answers=wrong_answers_cnt, questions=exam.questions,
                                             student=student)

        exam.correct_answers = exam.questions - wrong_answers_cnt
        exam.save()
        update_student_wrong_answers_in_exam.delay(student_id=student.id, wrong_question_ids=wrong_question_ids,
                                                   correct_question_ids=correct_question_ids)

        return data


class CategoryMixExamAnswerSerializer(CategoryExamAnswerSerializer):
    exam_id = None
    wrong_questions = serializers.ListSerializer(child=QuestionAnswerSerializer(), max_length=settings.MAX_QUESTIONS)
    correct_questions = serializers.ListSerializer(child=QuestionAnswerSerializer(), max_length=settings.MAX_QUESTIONS)
    saved_questions = serializers.ListSerializer(child=QuestionAnswerSerializer(), max_length=settings.MAX_QUESTIONS)
    delete_saved_questions = serializers.ListSerializer(child=QuestionAnswerSerializer(),
                                                        max_length=settings.MAX_QUESTIONS)

    @transaction.atomic
    def to_internal_value(self, data):
        serializers.Serializer.to_internal_value(self, data)
        student = self.context['request'].user
        saved_questions = data['saved_questions']
        wrong_questions = data['wrong_questions']
        correct_questions = data['correct_questions']
        delete_saved_questions = data['delete_saved_questions']

        if len(wrong_questions) + len(correct_questions) > settings.MAX_QUESTIONS:
            raise ValidationError('max length')

        saved_question_ids = list(set(question['pk'] for question in saved_questions))
        wrong_question_ids = list(set(question['pk'] for question in wrong_questions))
        correct_question_ids = list(set(question['pk'] for question in correct_questions))
        delete_saved_question_ids = list(set(question['pk'] for question in delete_saved_questions))

        wrong_question_ids = [i for i in wrong_question_ids if i not in correct_question_ids]
        delete_saved_question_ids = [i for i in delete_saved_question_ids if i not in saved_question_ids]

        for question_ids in [correct_question_ids, wrong_question_ids, saved_question_ids, delete_saved_question_ids]:
            for pk in question_ids:
                if not Question.is_correct_question_id(question_id=pk):
                    raise ValidationError({'pk': 'not found'})

        try:
            objs = [StudentSavedQuestion(student=student, question_id=pk) for pk in saved_question_ids]
            StudentSavedQuestion.objects.bulk_create(objs)
        except IntegrityError:
            raise ValidationError({'saved_questions': 'already exists'})

        StudentSavedQuestion.objects.filter(id__in=delete_saved_question_ids, student=student).delete()

        wrong_answers_cnt = len(wrong_question_ids)
        all_questions_cnt = len(correct_question_ids) + wrong_answers_cnt
        StudentLastExamResult.objects.create(wrong_answers=wrong_answers_cnt, questions=all_questions_cnt,
                                             student=student)

        update_student_wrong_answers_in_exam.delay(student_id=student.id, wrong_question_ids=wrong_question_ids,
                                                   correct_question_ids=correct_question_ids)

        return data


class CategoryExamCreateSerializer(serializers.ModelSerializer):
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


class CategoryMixExamCreateSerializer(CategoryExamCreateSerializer):
    category_id = None

    def create(self, validated_data):
        return None

    class Meta:
        model = CategoryExamStudent
        fields = ['id', 'questions', 'difficulty_level']
