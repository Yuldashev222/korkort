from rest_framework import serializers

from api.v1.exams.models import CategoryExamStudent, CategoryExamStudentResult
from api.v1.general.utils import get_language
from api.v1.lessons.models import LessonStudent
from api.v1.questions.models import StudentSavedQuestion
from api.v1.questions.serializers.variants import VariantSerializer


class CategoryExamStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryExamStudent
        fields = ['questions', 'percent']


class CategoryExamStudentResultSerializer(serializers.ModelSerializer):
    # image = serializers.SerializerMethodField()
    image = serializers.URLField(
        default='http://16.171.170.49/media/chapters/1:%20836c4b38-fe8e-4ef2-9a9c-bab/lessons/1:%20905c9192-956f-4054-9ce1-161/images/Re_A8H4vJl.png')
    name = serializers.SerializerMethodField()
    detail = CategoryExamStudentSerializer(source='categoryexamstudent_set', many=True)

    class Meta:
        model = CategoryExamStudentResult
        exclude = ['student']

    def get_name(self, instance):
        return getattr(instance.category, 'name_' + get_language())

    # def get_image(self, instance):
    #     return self.context['request'].build_absolute_uri(instance.category.image.url)


class WrongQuestionsExamSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    question_text = serializers.SerializerMethodField()
    question_video = serializers.FileField(source='question.video')
    question_image = serializers.ImageField(source='question.image')
    lesson = serializers.SerializerMethodField()
    answer = serializers.CharField(source='question.answer')
    is_saved = serializers.SerializerMethodField()  # last

    variant_set = VariantSerializer(source='question.variant_set', many=True)

    def get_is_saved(self, instance):
        student = self.context['request'].user
        try:
            StudentSavedQuestion.objects.get(question=instance.question, student=student)
        except StudentSavedQuestion.DoesNotExist:
            return False
        return True

    def get_question_text(self, instance):
        return getattr(instance.question, 'text_' + get_language())

    def get_lesson(self, instance):
        student = self.context['request'].user
        return LessonStudent.objects.get(student=student, lesson=instance.question.lesson).id  # last
