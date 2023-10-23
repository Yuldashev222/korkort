from django import forms
from django.contrib import admin
from django.utils.html import format_html

from api.v1.general.admin import AbstractTabularInline, AbstractStackedInline
from api.v1.questions.models import Category, Variant, Question, QuestionDetail, CategoryDetail


class VariantInlineFormset(forms.models.BaseInlineFormSet):
    def clean(self):
        super().clean()
        temp = []
        langs = []
        trues = {}
        for form in self.forms:
            if form.cleaned_data.get('language'):
                obj = (form.cleaned_data['language'], form.cleaned_data['is_correct'])
                if obj in temp and obj[1]:
                    raise forms.ValidationError("Each question must have exactly one correct option.")
                else:
                    temp.append(obj)
                    langs.append(obj[0])

                    if obj[1]:
                        if trues.get(obj[0]):
                            trues[obj[0]] += 1
                        else:
                            trues[obj[0]] = 1
                    else:
                        trues[obj[0]] = 0

        if 0 in trues.values():
            raise forms.ValidationError("Each question must have exactly one correct option.")

        for lang in langs:
            cnt = langs.count(lang)
            if not (2 <= cnt <= 4):
                raise forms.ValidationError("options in each language must be in the range [2, 4].")


class VariantInline(admin.TabularInline):
    model = Variant
    formset = VariantInlineFormset
    min_num = 2
    extra = 10


class QuestionDetailInline(AbstractStackedInline):
    model = QuestionDetail


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['ordering_number', 'category', 'difficulty_level']
    list_filter = ['ordering_number', 'category', 'lesson', 'difficulty_level']
    inlines = (VariantInline, QuestionDetailInline)

    fields = ['ordering_number', 'category', 'difficulty_level', 'lesson', 'image', 'gif']


class CategoryDetailInline(AbstractTabularInline):
    model = CategoryDetail


@admin.register(Category)
class QuestionCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'img']
    inlines = (CategoryDetailInline,)

    def img(self, obj):
        if obj.image:
            return format_html(f"<a href='{obj.image.url}'><img width=80 height=45 src='{obj.image.url}'></a>")
        return '-'
