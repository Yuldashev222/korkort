from django.contrib import admin

from api.v1.questions.models import QuestionCategory, Variant, Question


class LessonVariantInline(admin.TabularInline):
    model = Variant


class ExamVariantInline(admin.TabularInline):
    model = Variant


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id']
    inlines = (ExamVariantInline,)


@admin.register(QuestionCategory)
class QuestionCategoryAdmin(admin.ModelAdmin):
    list_display = ['id']
