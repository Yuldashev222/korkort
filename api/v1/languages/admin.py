from django.contrib import admin

from api.v1.languages.models import Language


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'ordering_number', 'is_active']
    list_display_links = ['pk', 'name']
    ordering = ['ordering_number']
