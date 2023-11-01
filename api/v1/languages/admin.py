from django.contrib import admin

from api.v1.languages.models import Language


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['language_id', 'name', 'ordering_number', 'is_active']
    list_display_links = ['language_id', 'name']
    ordering = ['ordering_number']
