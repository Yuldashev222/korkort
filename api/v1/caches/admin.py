from django.contrib import admin

from api.v1.caches.models import SetCache


@admin.register(SetCache)
class SetCacheAdmin(admin.ModelAdmin):
    list_display = ['clear_cache']
    list_display_links = None
    list_editable = list_display

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
