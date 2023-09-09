from django.contrib import admin
from django.utils.html import format_html

from api.v1.chapters.models import Chapter, ChapterStudent


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = [
        'ordering_number',
        'img',
        'title_en',
        'title_swe',
        'title_e_swe',
        'lessons',
    ]
    fields = [
        'ordering_number',
        'image',
        'title_swe',
        'title_e_swe',
        'title_en',
        'desc_swe',
        'desc_e_swe',
        'desc_en',
        'lessons'
    ]
    readonly_fields = [
        'lessons'
    ]
    list_display_links = ['title_en', 'title_swe', 'title_e_swe']
    search_fields = ['title_en', 'title_swe', 'title_e_swe']

    def img(self, obj):
        if obj.image:
            return format_html(f"<a href='{obj.image.url}'><img width=80 height=45 src='{obj.image.url}'></a>")
