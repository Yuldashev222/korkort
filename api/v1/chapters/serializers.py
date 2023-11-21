from rest_framework import serializers
from django.utils.timezone import now

from api.v1.general.utils import bubble_search
from api.v1.lessons.serializers import LessonListSerializer


class ChapterSerializer(serializers.Serializer):
    old_obj_all_lessons = None
    old_obj_completed_lessons = None
    obj_completed_lessons = None

    pk = serializers.IntegerField()
    image = 'https://www.industrialempathy.com/img/remote/ZiClJf-1920w.jpg'
    title = serializers.SerializerMethodField()
    lessons = serializers.IntegerField()
    chapter_hour = serializers.IntegerField()
    chapter_minute = serializers.IntegerField()
    completed_lessons = serializers.SerializerMethodField()
    is_open = serializers.SerializerMethodField()

    def get_completed_lessons(self, instance):
        temp = 0
        sort_list = self.context['chapter_student_list']
        obj = bubble_search(instance.pk, 'chapter_id', sort_list)
        if obj is not None:
            temp = obj['completed_lessons']
        self.obj_completed_lessons = temp
        return temp

    def get_is_open(self, instance):
        temp = LessonListSerializer.play
        if self.old_obj_completed_lessons is None:
            temp = LessonListSerializer.play

        elif self.context['request'].user.tariff_expire_date <= now().date():
            temp = LessonListSerializer.buy_clock

        elif self.old_obj_completed_lessons < self.old_obj_all_lessons:
            temp = LessonListSerializer.clock

        self.old_obj_all_lessons = instance.lessons
        self.old_obj_completed_lessons = self.obj_completed_lessons
        return temp

    def get_title(self, instance):
        sort_list = self.context['details']
        obj = bubble_search(instance.pk, 'chapter_id', sort_list)
        return obj['title']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['image'] = self.image
        return ret
