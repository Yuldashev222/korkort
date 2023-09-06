from rest_framework import serializers

from api.v1.exams.models import CategoryExamStudent


class ExamStudentCategorySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    category = serializers.CharField(source='category.name')

    class Meta:
        model = CategoryExamStudent
        exclude = ['student']

    def get_image(self, instance):
        return self.context['request'].build_absolute_uri(instance.category.image.url)
