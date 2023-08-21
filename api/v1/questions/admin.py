from django.contrib import admin

from api.v1.questions.models import LessonQuestion, QuestionCategory, LessonVariant


class LessonVariantInline(admin.TabularInline):
    model = LessonVariant
    fk_name = 'lesson_question'


@admin.register(LessonQuestion)
class LessonQuestionAdmin(admin.ModelAdmin):
    list_display = ['id']
    inlines = (LessonVariantInline,)


@admin.register(QuestionCategory)
class QuestionCategoryAdmin(admin.ModelAdmin):
    list_display = ['id']
