from django.contrib import admin

from api.v1.chapters.models import Chapter


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ['id', 'ordering_number']