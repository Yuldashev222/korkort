from django.db import transaction
from django.conf import settings
from rest_framework import serializers
from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError

from api.v1.exams.models import CategoryExamStudent, CategoryExamStudentResult, StudentLastExamResult
from api.v1.general.utils import bubble_search
from api.v1.questions.tasks import update_student_wrong_answers, update_student_correct_answers
from api.v1.questions.models import Question, Category


class CategoryExamStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryExamStudent
        fields = ['questions', 'percent']


class CategoryExamStudentResultSerializer(serializers.ModelSerializer):
    test_image = 'https://www.industrialempathy.com/img/remote/ZiClJf-1920w.jpg'

    pk = serializers.IntegerField(source='category_id')
    name = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()  # last
    detail = serializers.SerializerMethodField()

    def get_image(self, instance):
        return self.test_image

    def get_name(self, instance):
        sort_list = self.context['category_name_list']
        obj = bubble_search(instance.category_id, 'category_id', sort_list)
        if obj is not None:
            return obj['name']
        return '-'

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
        fields = ['pk', 'name', 'image', 'detail']


class CategoryExamAnswerSerializer(serializers.Serializer):
    category_id = serializers.IntegerField()
    wrong_question_id_list = serializers.ListField(child=serializers.IntegerField(),
                                                   max_length=settings.MAX_CATEGORY_QUESTIONS)
    correct_question_id_list = serializers.ListField(child=serializers.IntegerField(),
                                                     max_length=settings.MAX_CATEGORY_QUESTIONS)

    @transaction.atomic
    def to_internal_value(self, data):
        super().to_internal_value(data)
        student = self.context['request'].user
        category_id = data['category_id']
        wrong_question_id_list = list(set(data['wrong_question_id_list']))
        correct_question_id_list = list(set(data['correct_question_id_list']))
        correct_question_id_list = [i for i in correct_question_id_list if i not in wrong_question_id_list]

        all_question_count = len(wrong_question_id_list) + len(correct_question_id_list)
        if all_question_count > settings.MAX_CATEGORY_QUESTIONS:
            raise ValidationError({'detail': 'max length'})

        elif all_question_count < settings.MIN_QUESTIONS:
            raise ValidationError({'detail': 'min length'})

        try:
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            raise ValidationError({'category_id': 'not found'})

        for question_ids in [correct_question_id_list, wrong_question_id_list]:  # last
            for pk in question_ids:
                if not Question.is_correct_question_id(question_id=pk):
                    raise ValidationError({'question_id': 'not found'})

        wrong_question_count = len(wrong_question_id_list)
        correct_question_count = len(correct_question_id_list)

        StudentLastExamResult.objects.create(wrong_answers=wrong_question_count, questions=all_question_count,
                                             student_id=student.pk)

        result, _ = CategoryExamStudentResult.objects.get_or_create(category_id=category.pk, student_id=student.pk)
        CategoryExamStudent.objects.create(result_id=result.pk, correct_answers=correct_question_count,
                                           questions=all_question_count)

        update_student_correct_answers(student=student, wrong_question_ids=wrong_question_id_list,
                                       correct_question_ids=correct_question_id_list)
        update_student_wrong_answers.delay(student_id=student.pk, wrong_question_ids=wrong_question_id_list,
                                           correct_question_ids=correct_question_id_list)

        return data


class CategoryMixExamAnswerSerializer(CategoryExamAnswerSerializer):
    category_id = None
    wrong_question_id_list = serializers.ListField(child=serializers.IntegerField(),
                                                   max_length=settings.MAX_CATEGORY_MIX_QUESTIONS)
    correct_question_id_list = serializers.ListField(child=serializers.IntegerField(),
                                                     max_length=settings.MAX_CATEGORY_MIX_QUESTIONS)

    @transaction.atomic
    def to_internal_value(self, data):
        serializers.Serializer.to_internal_value(self, data)
        student = self.context['request'].user
        wrong_question_id_list = list(set(data['wrong_question_id_list']))
        correct_question_id_list = list(set(data['correct_question_id_list']))
        correct_question_id_list = [i for i in correct_question_id_list if i not in wrong_question_id_list]

        all_question_count = len(wrong_question_id_list) + len(correct_question_id_list)
        if all_question_count > settings.MAX_CATEGORY_MIX_QUESTIONS:
            raise ValidationError({'detail': 'max length'})

        elif all_question_count < settings.MIN_QUESTIONS:
            raise ValidationError({'detail': 'min length'})

        for question_ids in [correct_question_id_list, wrong_question_id_list]:  # last
            for pk in question_ids:
                if not Question.is_correct_question_id(question_id=pk):
                    raise ValidationError({'question_id': 'not found'})

        wrong_question_count = len(wrong_question_id_list)

        StudentLastExamResult.objects.create(wrong_answers=wrong_question_count, questions=all_question_count,
                                             student_id=student.pk)

        update_student_correct_answers(student=student, wrong_question_ids=wrong_question_id_list,
                                       correct_question_ids=correct_question_id_list)
        update_student_wrong_answers.delay(student_id=student.pk, wrong_question_ids=wrong_question_id_list,
                                           correct_question_ids=correct_question_id_list)

        return data


class CategoryExamCreateSerializer(serializers.Serializer):
    category_id = serializers.IntegerField()
    difficulty_level = serializers.ChoiceField(choices=Question.DIFFICULTY_LEVEL, allow_null=True)
    counts = serializers.IntegerField(validators=[MinValueValidator(settings.MIN_QUESTIONS),
                                                  MaxValueValidator(settings.MAX_CATEGORY_QUESTIONS)])

    def validate_category_id(self, cat_id):
        get_object_or_404(Category, pk=cat_id)
        return cat_id


class CategoryMixExamCreateSerializer(serializers.Serializer):
    difficulty_level = serializers.ChoiceField(choices=Question.DIFFICULTY_LEVEL, allow_null=True)
    counts = serializers.IntegerField(validators=[MinValueValidator(settings.MIN_QUESTIONS),
                                                  MaxValueValidator(settings.MAX_QUESTIONS)])
    category_id_list = serializers.ListField(child=serializers.IntegerField(), min_length=2)

    def validate_category_id_list(self, lst):
        lst = list(set(lst))
        trust_category_id_list = list(Category.objects.values_list('pk', flat=True))
        for i in lst:
            if i not in trust_category_id_list:
                raise ValidationError('not found')
        return lst
