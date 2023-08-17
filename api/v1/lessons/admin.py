from django.contrib import admin

from .models import Lesson


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['id']
    fieldsets = (
        ('Titles', {
            'fields': ('title_swe', 'title_easy_swe', 'title_en'),
        }),
        ('Videos', {
            'fields': ('image', 'video_swe', 'video_easy_swe', 'video_en'),
        }),
        ('Texts', {
            'fields': ('text_swe', 'text_easy_swe', 'text_en'),
        }),
    )
    # fields = [
    #
    #     ,
    #
    # ]
