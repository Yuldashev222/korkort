from django.contrib import admin

from api.v1.lessons.models import Lesson


class LessonSourceFilter(admin.SimpleListFilter):
    title = 'Lessons'
    parameter_name = 'lesson'

    def lookups(self, request, model_admin):
        chapter_id = request.GET.get('lesson_detail__lesson__chapter__id__exact')
        if chapter_id:
            return [(lesson.pk, lesson) for lesson in Lesson.objects.filter(chapter_id=chapter_id)]
        return ((None, None),)

    def queryset(self, request, queryset):
        lesson_id = self.value()
        chapter_id = request.GET.get('lesson_detail__lesson__chapter__id__exact')
        print(lesson_id, chapter_id)
        if lesson_id and chapter_id:
            return queryset.filter(lesson_detail__lesson_id=lesson_id)
        return queryset
