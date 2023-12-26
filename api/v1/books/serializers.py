from django.utils.timezone import now
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied

from api.v1.books.models import BookChapterStudent, BookChapter
from api.v1.general.utils import bubble_search


class BookChapterSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    is_open = serializers.BooleanField()
    is_completed = serializers.SerializerMethodField()

    def get_is_completed(self, instance):
        sort_list = self.context['student_chapter_list']
        obj = bubble_search(instance.pk, 'chapter_id', sort_list)
        return bool(obj and obj['is_completed'])


class BookListSerializer(serializers.Serializer):
    title = serializers.CharField()
    chapters = BookChapterSerializer(source='bookchapter_set', many=True)


class BookDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookChapter
        fields = ['pk', 'audio', 'content']


class BookChapterStudentSerializer(serializers.Serializer):
    student = serializers.HiddenField(default=serializers.CurrentUserDefault())
    chapter_id = serializers.IntegerField()
    is_completed = serializers.BooleanField()

    def validate_chapter_id(self, value):
        try:
            chapter = BookChapter.objects.get(pk=value)
        except BookChapter.DoesNotExist:
            raise ValidationError('chapter_id does not exist')
        if not chapter.is_open and self.context['request'].user.tariff_expire_date <= now().date():
            raise PermissionDenied('You do not have permission to')
        return value

    def create(self, validated_data):
        is_completed = validated_data.pop('is_completed')
        obj, _ = BookChapterStudent.objects.get_or_create(**validated_data)
        if obj.is_completed != is_completed:
            obj.is_completed = is_completed
            obj.save()
        return obj
