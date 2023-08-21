from django.contrib import admin

from .models import Lesson, LessonStudent, LessonWordInfo, LessonSource


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['id']
    fieldsets = (
        ('Main', {
            'fields': ('chapter', 'is_open', 'lesson_time', 'ordering_number'),
        }),
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


@admin.register(LessonStudent)
class LessonStudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'is_completed']


@admin.register(LessonWordInfo)
class LessonWordInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'text']


@admin.register(LessonSource)
class LessonSourceAdmin(admin.ModelAdmin):
    list_display = ['id', 'text']
