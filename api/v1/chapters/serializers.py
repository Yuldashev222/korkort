from rest_framework import serializers
from django.utils.timezone import now

from api.v1.general.utils import bubble_search
from api.v1.chapters.models import Chapter
from api.v1.lessons.serializers import LessonListSerializer


class ChapterSerializer(serializers.ModelSerializer):
    obj_completed_lessons = None
    old_obj_chapter_lessons = None
    old_obj_completed_lessons = None

    # image = serializers.ImageField()
    image = 'https://www.industrialempathy.com/img/remote/ZiClJf-1920w.jpg'
    title = serializers.SerializerMethodField()
    lessons = serializers.IntegerField()
    chapter_hour = serializers.IntegerField()
    chapter_minute = serializers.IntegerField()
    completed_lessons = serializers.SerializerMethodField()
    is_open = serializers.SerializerMethodField()

    def get_is_open(self, instance):
        temp = LessonListSerializer.play

        if not (self.old_obj_completed_lessons is not None or self.old_obj_chapter_lessons is not None):
            temp = LessonListSerializer.play

        elif self.context['request'].user.tariff_expire_date <= now():
            temp = LessonListSerializer.buy_clock

        elif self.old_obj_completed_lessons < self.old_obj_chapter_lessons:
            temp = LessonListSerializer.clock

        self.old_obj_completed_lessons = self.obj_completed_lessons
        self.old_obj_chapter_lessons = instance.lessons
        return temp

    def get_completed_lessons(self, instance):
        sort_list = self.context['chapter_student_list']
        obj = bubble_search(instance.id, 'chapter', sort_list)
        if obj is not None:
            if self.obj_completed_lessons is not None:
                self.obj_completed_lessons = obj['completed_lessons']
            return obj['completed_lessons']
        return 0

    def get_title(self, instance):
        sort_list = self.context['details']
        obj = bubble_search(instance.id, 'chapter', sort_list)
        if obj is not None:
            return obj['title']
        return '-'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['image'] = self.image
        return ret

    class Meta:
        model = Chapter
        fields = ['id', 'title', 'lessons', 'chapter_hour', 'chapter_minute', 'completed_lessons', 'is_open']
