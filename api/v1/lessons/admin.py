from django.contrib import admin
from django.utils.html import format_html

from .filters import LessonSourceFilter
from .models import Lesson, LessonWordInfo, LessonSource, LessonDetail
from api.v1.general.admin import AbstractStackedInline, AbstractTabularInline


class LessonDetailInline(AbstractStackedInline):
    model = LessonDetail


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['chapter', 'ordering_number', 'img', 'is_open', 'lesson_time']
    list_display_links = ['chapter', 'ordering_number']
    inlines = [LessonDetailInline]
    list_filter = ['chapter']
    ordering = ('chapter__ordering_number', 'ordering_number')

    def chapter(self, obj):
        return obj.chapter

    def img(self, obj):
        if obj.image:
            return format_html(f"<a href='{obj.image.url}'><img width=80 height=45 src='{obj.image.url}'></a>")
        return '-'

    fieldsets = (
        ('Main', {
            'fields': ('chapter', 'image', 'is_open', 'lesson_time', 'ordering_number'),
        }),
    )


class LessonSourceInline(AbstractStackedInline):
    model = LessonSource
    min_num = None
    max_num = None
    extra = 5
    verbose_name = 'Source'
    verbose_name_plural = 'Sources'


class LessonWordInfoInline(LessonSourceInline):
    model = LessonWordInfo
    verbose_name = 'Word Info'
    verbose_name_plural = 'Word Infos'


@admin.register(LessonDetail)
class LessonDetailAdmin(admin.ModelAdmin):
    list_display = ['language', 'lesson', 'title', 'video']
    list_display_links = ['lesson', 'language', 'title']
    search_fields = ['title', 'text']
    list_filter = ['lesson__chapter', 'language']
    list_select_related = ('lesson__chapter', 'language')
    readonly_fields = ['lesson']
    inlines = (LessonSourceInline, LessonWordInfoInline)
    fields = (
        'language',
        'lesson',
        'title',
        'video',
        'text'
    )


@admin.register(LessonSource)
class LessonSourceAdmin(admin.ModelAdmin):
    list_display = ['chapter', 'lesson', 'language', 'text', 'source_link']
    list_display_links = ['chapter', 'lesson', 'language', 'text']
    list_filter = ['lesson_detail__lesson__chapter', LessonSourceFilter, 'lesson_detail__language']
    search_fields = ['text', 'link']
    ordering = ['-pk']
    readonly_fields = ('lesson_detail',)
    fields = ('lesson_detail', 'text', 'link')

    list_select_related = ('lesson_detail__lesson', 'lesson_detail__lesson__chapter', 'lesson_detail__language')

    def chapter(self, obj):
        return obj.lesson_detail.lesson.chapter

    def lesson(self, obj):
        return obj.lesson_detail.lesson

    def language(self, obj):
        return obj.lesson_detail.language

    def source_link(self, obj):
        return format_html(f"<a href='{obj.link}'>{obj.link}</a>")

    def has_add_permission(self, request):
        return False


@admin.register(LessonWordInfo)
class LessonWordInfoAdmin(LessonSourceAdmin):
    list_display = ['chapter', 'lesson', 'language', 'word']
    list_display_links = list_display
    search_fields = ['word', 'info']
    fields = ('lesson_detail', 'word', 'info')
