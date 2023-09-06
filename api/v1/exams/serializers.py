from rest_framework import serializers

from api.v1.exams.models import CategoryExamStudent
from api.v1.general.utils import get_language


class ExamStudentCategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = CategoryExamStudent
        exclude = ['student']

    def get_category_name(self, instance):
        return getattr(instance, 'name_' + get_language())

    def get_image(self, instance):
        return self.context['request'].build_absolute_uri(instance.category.image.url)
