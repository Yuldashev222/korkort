from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from api.v1.general.admin import AbstractStackedInline
from api.v1.questions.models import Question, QuestionDetail
from api.v1.questions.filters import QuestionLessonFilter, QuestionDetailLessonFilter


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
    list_display = ['pk', 'category_id', 'difficulty_level', 'lesson', 'video']
    list_display_links = ['pk', 'category_id', 'difficulty_level', 'lesson']
    list_filter = ('category_id', 'difficulty_level', 'lesson__chapter', QuestionLessonFilter)
    inlines = (QuestionDetailInline,)
    list_select_related = ('lesson',)
    ordering = ['-pk']
    fields = ['category_id', 'difficulty_level', 'image', 'video', 'lesson', 'ordering_number', ]


@admin.register(QuestionDetail)
class QuestionDetailAdmin(admin.ModelAdmin):
    list_display = ['language', 'question_id', 'difficulty_level', 'lesson', 'question_text']
    list_display_links = ['language', 'question_id', 'difficulty_level', 'lesson']
    list_filter = ['language', 'question__category_id', 'question__difficulty_level', 'question__lesson__chapter',
                   QuestionDetailLessonFilter
                   ]
    search_fields = ['text', 'answer', 'correct_variant', 'variant2', 'variant3', 'variant4']
    readonly_fields = ('question',)
    fields = ('question', 'language', 'text', 'correct_variant', 'variant2', 'variant3', 'variant4', 'answer')
    list_select_related = ('question__lesson', 'question__category_id', 'language',)

    def question_text(self, obj):
        return mark_safe(obj.text)

    def category(self, obj):
        return obj.question.category

    category.admin_order_field = 'question__category_id'  # last

    def lesson(self, obj):
        return obj.question.lesson

    lesson.admin_order_field = 'question__lesson'

    def difficulty_level(self, obj):
        return obj.question.get_difficulty_level_display()

    difficulty_level.admin_order_field = 'question__difficulty_level'

    def has_add_permission(self, request):
        return False
