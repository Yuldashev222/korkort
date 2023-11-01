from django import forms
from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from api.v1.general.admin import AbstractStackedInline
from api.v1.lessons.models import Lesson
from api.v1.questions.filters import QuestionLessonFilter, QuestionDetailLessonFilter
from api.v1.questions.models import Category, Question, QuestionDetail, CategoryDetail


class CategoryDetailInline(AbstractStackedInline):
    model = CategoryDetail


@admin.register(Category)
class QuestionCategoryAdmin(admin.ModelAdmin):
    list_display = ['ordering_number', 'img']
    inlines = (CategoryDetailInline,)

    def img(self, obj):
        if obj.image:
            return format_html(f"<a href='{obj.image.url}'><img width=80 height=45 src='{obj.image.url}'></a>")
        return '-'


class VariantInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        super().clean()
        correct_variants = 0
        for form in self.forms:
            if form.cleaned_data['is_correct']:
                correct_variants += 1
        if correct_variants != 1:
            raise forms.ValidationError("Each question must have exactly one correct option.")


class QuestionDetailInline(AbstractStackedInline):
    model = QuestionDetail


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['pk', 'category', 'difficulty_level', 'lesson', 'gif']
    list_display_links = ['pk', 'category', 'difficulty_level', 'lesson']
    list_filter = ('category', 'difficulty_level', 'lesson__chapter', QuestionLessonFilter)
    inlines = (QuestionDetailInline,)
    list_select_related = ('lesson', 'category')
    ordering = ['-pk']
    fields = ['category', 'difficulty_level', 'image', 'gif', 'lesson', 'ordering_number', ]


@admin.register(QuestionDetail)
class QuestionDetailAdmin(admin.ModelAdmin):
    list_display = ['language', 'question_id', 'category', 'difficulty_level', 'lesson', 'question_text']
    list_display_links = ['language', 'question_id', 'category', 'difficulty_level', 'lesson']
    list_filter = ['language', 'question__category', 'question__difficulty_level', 'question__lesson__chapter',
                   QuestionDetailLessonFilter
                   ]
    search_fields = ['text', 'answer', 'correct_variant', 'variant2', 'variant3', 'variant4']
    readonly_fields = ('question',)
    fields = ('question', 'language', 'text', 'correct_variant', 'variant2', 'variant3', 'variant4', 'answer')
    list_select_related = ('question__lesson', 'question__category', 'language',)

    def question_text(self, obj):
        return mark_safe(obj.text)

    def category(self, obj):
        return obj.question.category

    category.admin_order_field = 'question__category'

    def lesson(self, obj):
        return obj.question.lesson

    lesson.admin_order_field = 'question__lesson'

    def difficulty_level(self, obj):
        return obj.question.get_difficulty_level_display()

    difficulty_level.admin_order_field = 'question__difficulty_level'

    def has_add_permission(self, request):
        return False
