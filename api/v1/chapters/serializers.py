from rest_framework import serializers
from django.utils.timezone import now

from api.v1.general.utils import get_language
from api.v1.chapters.models import ChapterStudent
from api.v1.lessons.serializers import LessonListSerializer


class ChapterStudentSerializer(serializers.ModelSerializer):
    old_obj = None
    old_obj_chapter_lessons = None
    title = serializers.SerializerMethodField()
    desc = serializers.SerializerMethodField()
    # image = serializers.ImageField(source='chapter.image', max_length=300)
    image = serializers.URLField(
        default='https://www.e-report.uz/media/chapters/1%3A%202014e1e9-a989-4995-b36f-77a/images/IMG.png')
    lessons = serializers.IntegerField(source='chapter.lessons')
    chapter_hour = serializers.IntegerField(source='chapter.chapter_hour')
    chapter_minute = serializers.IntegerField(source='chapter.chapter_minute')
    is_open = serializers.SerializerMethodField()

    class Meta:
        model = ChapterStudent
        fields = [
            'id', 'title', 'desc', 'image', 'lessons', 'chapter_hour', 'chapter_minute', 'completed_lessons', 'is_open'
        ]

    def get_title(self, instance):
        return getattr(instance.chapter, 'title_' + get_language())

    def get_desc(self, instance):
        return getattr(instance.chapter, 'desc_' + get_language())

    def get_is_open(self, instance):
        temp = LessonListSerializer.play

        if not (self.old_obj and self.old_obj_chapter_lessons):
            temp = LessonListSerializer.play

        elif self.context['request'].user.tariff_expire_date <= now():
            temp = LessonListSerializer.buy_clock

        elif self.old_obj.completed_lessons < self.old_obj_chapter_lessons:
            temp = LessonListSerializer.clock

        self.old_obj = instance
        self.old_obj_chapter_lessons = instance.chapter.lessons
        return temp
