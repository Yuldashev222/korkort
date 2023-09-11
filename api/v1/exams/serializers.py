from rest_framework import serializers

from api.v1.exams.models import CategoryExamStudent, CategoryExamStudentResult
from api.v1.general.utils import get_language
from api.v1.lessons.models import LessonStudent
from api.v1.questions.serializers.exams import QuestionExamSerializer
from api.v1.questions.serializers.variants import VariantSerializer


class CategoryExamStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryExamStudent
        exclude = ['student']


class CategoryExamStudentResultSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    detail = CategoryExamStudentSerializer(source='categoryexamstudent_set', many=True)

    class Meta:
        model = CategoryExamStudentResult
        exclude = ['student']

    def get_name(self, instance):
        return getattr(instance.category, 'name_' + get_language())

    def get_image(self, instance):
        return self.context['request'].build_absolute_uri(instance.category.image.url)


class WrongQuestionsExamSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    question_text = serializers.SerializerMethodField()
    question_video = serializers.FileField(source='question.video')
    question_image = serializers.ImageField(source='question.image')
    lesson = serializers.SerializerMethodField()
    answer = serializers.CharField(source='question.answer')

    variant_set = VariantSerializer(source='question.variant_set', many=True)

    def get_question_text(self, instance):
        return getattr(instance.question, 'text_' + get_language())

    def get_lesson(self, instance):
        student = self.context['request'].user
        return LessonStudent.objects.get(student=student, lesson=instance.question.lesson).id  # last
