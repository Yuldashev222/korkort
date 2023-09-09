from rest_framework import serializers

from api.v1.exams.models import CategoryExamStudent, CategoryExamStudentResult
from api.v1.general.utils import get_language


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
