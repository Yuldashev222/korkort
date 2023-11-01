from django.contrib import admin

from api.v1.levels.models import Level, LevelDetail
from api.v1.general.admin import AbstractStackedInline


class LevelDetailInline(AbstractStackedInline):
    model = LevelDetail


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ['ordering_number', 'correct_answers']
    list_display_links = list_display
    inlines = [LevelDetailInline]
    ordering = ['ordering_number']
