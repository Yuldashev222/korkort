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
    readonly_fields = ('correct_answers', 'ordering_number')
    ordering = ['ordering_number']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
