from rest_framework import serializers

from api.v1.chapters.models import Chapter


class ChapterSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    desc = serializers.SerializerMethodField()

    class Meta:
        model = Chapter
        fields = ['title', 'desc', 'image', 'lessons', 'chapter_hour', 'chapter_minute']

    def get_title(self, instance):
        language = self.context['request'].query_params.get('language')
        if language not in ['en', 'swe', 'easy_swe']:
            return ''
        return getattr(instance, 'title_' + language, '')

    def get_desc(self, instance):
        language = self.context['request'].query_params.get('language')
        if language not in ['en', 'swe', 'easy_swe']:
            return ''
        return getattr(instance, 'desc_' + language, '')
