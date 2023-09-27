from django.db import transaction, IntegrityError
from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.v1.exams.models import CategoryExamStudent, CategoryExamStudentResult, StudentLastExamResult
from api.v1.general.utils import get_language
from api.v1.questions.tasks import update_student_wrong_answers
from api.v1.questions.models import Question, StudentSavedQuestion, Category
from api.v1.questions.serializers.questions import QuestionAnswerSerializer


class CategoryExamStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryExamStudent
        fields = ['questions', 'percent']


class CategoryExamStudentResultSerializer(serializers.ModelSerializer):
    # image = serializers.SerializerMethodField()
    image = serializers.URLField(
        default='http://91.226.221.227/media/chapters/1%3A_5663e70a-0c7b-4118-907a-be4/images/Rectangle_625.png')
    name = serializers.SerializerMethodField()
    detail = serializers.SerializerMethodField()

    def get_detail(self, instance):
        last_exams = instance.categoryexamstudent_set.all()[:10]
        data = CategoryExamStudentSerializer(last_exams, many=True).data
        len_data = len(data)
        if len_data < 10:
            obj = {'questions': 0, 'percent': 0}
            data.extend([obj] * (10 - len_data))
        data.reverse()
        return data

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

    @transaction.atomic
    def to_internal_value(self, data):
        super().to_internal_value(data)
        student = self.context['request'].user
        exam_id = data['exam_id']
        wrong_questions = data['wrong_questions']
        correct_questions = data['correct_questions']

        if len(wrong_questions) + len(correct_questions) > settings.MAX_QUESTIONS:
            raise ValidationError({'detail': 'max length'})

        if len(wrong_questions) + len(correct_questions) < 1:
            raise ValidationError({'detail': 'min length'})

        try:
            exam = CategoryExamStudent.objects.get(id=exam_id)
        except CategoryExamStudent.DoesNotExist:
            raise ValidationError({'exam_id': 'not found'})

        if exam.correct_answers > 0:
            raise ValidationError({'exam_id': 'not found'})

        wrong_question_ids = list(set(question['pk'] for question in wrong_questions))
        correct_question_ids = list(set(question['pk'] for question in correct_questions))

        wrong_question_ids = [i for i in wrong_question_ids if i not in correct_question_ids]

        for question_ids in [correct_question_ids, wrong_question_ids]:
            for pk in question_ids:
                if not Question.is_correct_question_id(question_id=pk):
                    raise ValidationError({'pk': 'not found'})

        wrong_answers_cnt = len(wrong_question_ids)
        StudentLastExamResult.objects.create(wrong_answers=wrong_answers_cnt, questions=exam.questions,
                                             student=student)

        exam.correct_answers = exam.questions - wrong_answers_cnt
        exam.save()
        update_student_wrong_answers.delay(student_id=student.id, wrong_question_ids=wrong_question_ids,
                                           correct_question_ids=correct_question_ids)

        return data


class CategoryMixExamAnswerSerializer(CategoryExamAnswerSerializer):
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

        update_student_wrong_answers.delay(student_id=student.id, wrong_question_ids=wrong_question_ids,
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
