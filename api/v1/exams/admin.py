from django.contrib import admin

from api.v1.exams.models import CategoryExamStudentResult


@admin.register(CategoryExamStudentResult)
class CategoryExamStudentResultAdmin(admin.ModelAdmin):
    list_display = ['category', 'student', 'avg']

    fields = list_display
    search_fields = ['student']
    list_filter = ['category', 'student']

    def avg(self, obj):
        return f'{obj.percent} %'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
