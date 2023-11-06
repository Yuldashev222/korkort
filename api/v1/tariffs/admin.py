from django.contrib import admin

from .models import Tariff


@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ['days', 'price', 'is_active']
    list_display_links = ['days', 'price']
    list_filter = ['is_active']
    ordering = ['days']
    fields = ['days', 'price', 'is_active']
