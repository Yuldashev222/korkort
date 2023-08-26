from rest_framework import serializers

from api.v1.chapters.models import ChapterStudent
from api.v1.lessons.models import LessonStudent


class ChapterSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    desc = serializers.SerializerMethodField()
    image = serializers.ImageField(source='chapter.image')
    lessons = serializers.IntegerField(source='chapter.lessons')
    chapter_hour = serializers.IntegerField(source='chapter.chapter_hour')
    chapter_minute = serializers.IntegerField(source='chapter.chapter_minute')

    class Meta:
        model = ChapterStudent
        fields = ['title', 'desc', 'image', 'lessons', 'chapter_hour', 'chapter_minute', 'completed_lessons']

    def get_title(self, instance):
        language = self.context['request'].query_params.get('language')
        if language not in ['en', 'swe', 'e_swe']:
            return ''
        return getattr(instance.chapter, 'title_' + language, '')

    def get_desc(self, instance):
        language = self.context['request'].query_params.get('language')
        if language not in ['en', 'swe', 'e_swe']:
            return ''
        return getattr(instance.chapter, 'desc_' + language, '')
