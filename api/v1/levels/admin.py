from django.contrib import admin

from api.v1.levels.models import Level, LevelDetail


class LevelDetailInline(admin.TabularInline):
    model = LevelDetail


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ['ordering_number', 'correct_answers']
    list_display_links = list_display
    inlines = [LevelDetailInline]
