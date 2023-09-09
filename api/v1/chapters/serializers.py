from rest_framework import serializers
from django.utils.timezone import now

from api.v1.general.utils import get_language
from api.v1.chapters.models import ChapterStudent


class ChapterSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    desc = serializers.SerializerMethodField()
    image = serializers.ImageField(source='chapter.image', max_length=300)
    lessons = serializers.IntegerField(source='chapter.lessons')
    chapter_hour = serializers.IntegerField(source='chapter.chapter_hour')
    chapter_minute = serializers.IntegerField(source='chapter.chapter_minute')
    is_open = serializers.SerializerMethodField()

    class Meta:
        model = ChapterStudent
        fields = [
            'id', 'title', 'desc', 'image', 'lessons', 'last_lesson',
            'chapter_hour', 'chapter_minute', 'completed_lessons', 'is_open'
        ]

    def get_title(self, instance):
        return getattr(instance.chapter, 'title_' + get_language())

    def get_desc(self, instance):
        return getattr(instance.chapter, 'desc_' + get_language())

    def get_is_open(self, instance):
        if not instance.is_open:
            return False
        if instance.student.tariff_expire_date > now():
            return True
        return False
