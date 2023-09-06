from rest_framework import serializers

from api.v1.exams.models import CategoryExamStudent


class ExamStudentCategorySerializer(serializers.ModelSerializer):
    image = serializers.ImageField(source='category.image')
    category = serializers.CharField(source='category.name')

    class Meta:
        model = CategoryExamStudent
        exclude = ['student']
