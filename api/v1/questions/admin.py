from django.contrib import admin

from api.v1.questions.models import LessonQuestion, QuestionCategory, Variant, ExamQuestion


class LessonVariantInline(admin.TabularInline):
    model = Variant
    fk_name = 'lesson_question'


@admin.register(LessonQuestion)
class LessonQuestionAdmin(admin.ModelAdmin):
    list_display = ['id']
    inlines = (LessonVariantInline,)


class ExamVariantInline(admin.TabularInline):
    model = Variant
    fk_name = 'exam_question'


@admin.register(ExamQuestion)
class ExamQuestionAdmin(admin.ModelAdmin):
    list_display = ['id']
    inlines = (ExamVariantInline,)


@admin.register(QuestionCategory)
class QuestionCategoryAdmin(admin.ModelAdmin):
    list_display = ['id']
