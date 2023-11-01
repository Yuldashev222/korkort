from rest_framework import serializers

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
        if obj is not None:
            return obj['is_completed']
        return False


class BookListSerializer(serializers.Serializer):
    title = serializers.CharField()
    chapters = BookChapterSerializer(source='bookchapter_set', many=True)


class BookDetailSerializer(serializers.ModelSerializer):
    is_completed = serializers.SerializerMethodField()

    class Meta:
        model = BookChapter
        fields = ['pk', 'title', 'audio', 'is_completed', 'content']

    def get_is_completed(self, instance):
        obj, _ = BookChapterStudent.objects.get_or_create(chapter_id=instance.pk,
                                                          student_id=self.context['request'].user.pk)
        return obj.is_completed


class BookChapterStudentSerializer(serializers.ModelSerializer):
    student = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = BookChapterStudent
        fields = ['chapter', 'student', 'is_completed']

    def create(self, validated_data):
        is_completed = validated_data.pop('is_completed')
        obj, _ = BookChapterStudent.objects.get_or_create(**validated_data)
        if obj.is_completed != is_completed:
            obj.is_completed = is_completed
            obj.save()
        return obj
