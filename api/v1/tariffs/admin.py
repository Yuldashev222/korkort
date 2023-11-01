from django.contrib import admin

from .models import Tariff


@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ['days', 'price', 'tariff_discount', 'student_discount', 'is_active']
    list_display_links = ['days', 'price']
    list_filter = ['tariff_discount', 'student_discount', 'is_active']

    fields = [
        'days',
        'price',
        'tariff_discount',
        'student_discount',
        'is_active',
        'tariff_discount_amount',
        'student_discount_amount',
        'created_at',
    ]
    readonly_fields = [
        'tariff_discount_amount',
        'student_discount_amount',
        'created_at',
    ]
