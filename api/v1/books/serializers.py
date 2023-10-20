from rest_framework import serializers

from api.v1.books.models import BookPart, BookChapterStudent
from api.v1.general.utils import bubble_search


class BookChapterSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='chapter_id')
    title = serializers.CharField()
    is_completed = serializers.SerializerMethodField()

    def get_is_completed(self, instance):
        sort_list = self.context['student_chapter_list']
        obj = bubble_search(instance['chapter_id'], 'chapter_id', sort_list)
        if obj is not None:
            return obj['is_completed']
        return False


class BookListSerializer(serializers.Serializer):
    title = serializers.SerializerMethodField()
    chapters = serializers.SerializerMethodField()

    def get_title(self, instance):
        sort_list = self.context['book_title_list']
        obj = bubble_search(instance.id, 'book_id', sort_list)
        if obj is not None:
            return obj['title']
        return '-'

    def get_chapters(self, instance):
        chapters = [i for i in self.context['chapters'] if i['chapter__book_id'] == instance.id]
        context = {'student_chapter_list': self.context['student_chapter_list']}
        serializer = BookChapterSerializer(chapters, many=True, context=context)
        return serializer.data


class BookPartSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = BookPart
        exclude = ['id', 'ordering_number', 'book_chapter']

    def get_image(self, instance):
        if not instance.image:
            return None
        return self.context['request'].build_absolute_uri(instance.image.url)


class BookDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='chapter_id')
    title = serializers.CharField()
    is_completed = serializers.BooleanField()
    audio = serializers.FileField()
    parts = serializers.SerializerMethodField()

    def get_parts(self, instance):
        parts = BookPart.objects.filter(book_chapter_id=instance.id).order_by('ordering_number')
        return BookPartSerializer(parts, many=True, context=self.context).data


class BookChapterStudentSerializer(serializers.Serializer):
    chapter_id = serializers.IntegerField()
    is_completed = serializers.BooleanField()

    def create(self, validated_data):
        student_id = self.context['request'].user.id
        obj, created = BookChapterStudent.objects.get_or_create(student_id=student_id, **validated_data)
        if not created:
            obj.delete()
        return obj