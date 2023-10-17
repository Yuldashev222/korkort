from django.contrib import admin
from django.utils.html import format_html

from .models import Lesson, LessonWordInfo, LessonSource, LessonDetail
from api.v1.general.admin import AbstractTabularInline


class LessonWordInfoInline(admin.TabularInline):
    model = LessonWordInfo


class LessonSourceInline(admin.TabularInline):
    model = LessonSource


class LessonDetailInline(AbstractTabularInline):
    model = LessonDetail


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['ordering_number', 'img', 'is_open', 'lesson_time']
    inlines = [LessonDetailInline, LessonWordInfoInline, LessonSourceInline]
    list_filter = ['chapter', 'ordering_number']

    def img(self, obj):
        if obj.image:
            return format_html(f"<a href='{obj.image.url}'><img width=80 height=45 src='{obj.image.url}'></a>")
        return '-'

    fieldsets = (
        ('Main', {
            'fields': ('chapter', 'image', 'is_open', 'lesson_time', 'ordering_number'),
        }),
    )


@admin.register(LessonDetail)
class LessonDetailAdmin(admin.ModelAdmin):
    list_display = ['lesson', 'language', 'title', 'video']
    list_display_links = ['lesson', 'language', 'title']
    search_fields = ['title', 'text']
    list_filter = ['lesson__chapter', 'language']
    list_select_related = ('lesson__chapter', 'language')
    readonly_fields = ['lesson']
    fields = (
        'language',
        'lesson',
        'title',
        'video',
        'text'
    )


@admin.register(LessonWordInfo)
class LessonWordInfoAdmin(admin.ModelAdmin):
    list_display = ['lesson', 'word']
    list_display_links = list_display
    list_filter = ['lesson']
    search_fields = ['word', 'info']


@admin.register(LessonSource)
class LessonSourceAdmin(admin.ModelAdmin):
    list_display = ['lesson', 'source_link', 'text']
    list_display_links = ['lesson', 'text']
    list_filter = ['lesson']
    search_fields = ['text', 'link']

    def source_link(self, obj):
        return format_html(f"<a href='{obj.link}'>{obj.link}</a>")
