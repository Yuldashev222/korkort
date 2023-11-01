from django.contrib import admin
from django.utils.html import format_html

from api.v1.general.admin import AbstractStackedInline
from api.v1.chapters.models import Chapter, ChapterDetail


class ChapterDetailInline(AbstractStackedInline):
    model = ChapterDetail
    verbose_name = 'Title'
    verbose_name_plural = 'Titles'


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ['ordering_number', 'img', 'lessons', 'chapter_hour', 'chapter_minute']
    list_display_links = ['ordering_number', 'lessons', 'chapter_hour', 'chapter_minute']
    fields = ['ordering_number', 'image', 'lessons']
    readonly_fields = ['lessons']
    inlines = [ChapterDetailInline]
    ordering = ['ordering_number']

    def img(self, obj):
        if obj.image:
            return format_html(f"<a href='{obj.image.url}'><img width=80 height=45 src='{obj.image.url}'></a>")
