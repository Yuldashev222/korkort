from django.contrib import admin
from django.utils.html import format_html

from .models import Lesson, LessonWordInfo, LessonSource, LessonDetail


class LessonWordInfoInline(admin.TabularInline):
    model = LessonWordInfo


class LessonSourceInline(admin.TabularInline):
    model = LessonSource


class LessonDetailInline(admin.TabularInline):
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
