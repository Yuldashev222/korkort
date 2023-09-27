from django.contrib import admin
from django.utils.html import format_html

from .models import Lesson, LessonStudent, LessonWordInfo, LessonSource


class LessonWordInfoInline(admin.TabularInline):
    model = LessonWordInfo


class LessonSourceInline(admin.TabularInline):
    model = LessonSource


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = [
        'ordering_number', 'img', 'title_swe', 'title_en', 'title_e_swe', 'is_open', 'lesson_time'
    ]
    list_display_links = ['title_swe', 'title_en', 'title_e_swe']
    inlines = [LessonWordInfoInline, LessonSourceInline]
    list_filter = ['chapter', 'ordering_number']
    search_fields = ['title_swe', 'title_en', 'title_e_swe']

    def img(self, obj):
        if obj.image:
            return format_html(f"<a href='{obj.image.url}'><img width=80 height=45 src='{obj.image.url}'></a>")
        return '-'

    fieldsets = (
        ('Main', {
            'fields': ('chapter', 'is_open', 'lesson_time', 'ordering_number'),
        }),
        ('Titles', {
            'fields': ('title_swe', 'title_e_swe', 'title_en'),
        }),
        ('Files', {
            'fields': ('image', 'video_swe', 'video_e_swe', 'video_en'),
        }),
        ('Texts', {
            'fields': ('text_swe', 'text_e_swe', 'text_en'),
        }),
    )


# @admin.register(LessonStudent)
# class LessonStudentAdmin(admin.ModelAdmin):
#     list_display = ['lesson', 'student', 'is_completed', 'ball']
#     list_display_links = ['lesson', 'student']
#     list_filter = ['lesson', 'student', 'is_completed']
#
#     def has_change_permission(self, request, obj=None):
#         return False
#
#     def has_add_permission(self, request, obj=None):
#         return False
#
#     def has_delete_permission(self, request, obj=None):
#         return False
#
#     def get_queryset(self, request):
#         return LessonStudent.objects.select_related('student', 'lesson')
#

@admin.register(LessonWordInfo)
class LessonWordInfoAdmin(admin.ModelAdmin):
    list_display = ['lesson', 'text_swe', 'text_en', 'text_e_swe']
    list_display_links = list_display
    list_filter = ['lesson']
    search_fields = ['text_swe', 'text_en', 'text_e_swe', 'info_swe', 'info_en', 'info_e_swe']


@admin.register(LessonSource)
class LessonSourceAdmin(admin.ModelAdmin):
    list_display = ['lesson', 'source_link', 'text_swe', 'text_en', 'text_e_swe']
    list_display_links = ['lesson', 'text_swe', 'text_en', 'text_e_swe']
    list_filter = ['lesson']
    search_fields = ['text_swe', 'text_en', 'text_e_swe', 'link']

    def source_link(self, obj):
        return format_html(f"<a href='{obj.link}'>{obj.link}</a>")
