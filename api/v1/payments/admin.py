from django.contrib import admin
from django.utils.html import format_html
from rangefilter.filters import DateRangeFilterBuilder

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_filter = ['tariff', 'use_bonus_money', 'is_paid', ('created_at', DateRangeFilterBuilder(title='Date'))]
    search_fields = [
        'order_id', 'student_email', 'called_student_email', 'student_name', 'called_student_name']

    list_display = [
        'ID', 'student_name', 'tariff', 'tariff_price', 'tariff_discount_amount', 'user_code_discount_amount',
        'student_bonus_amount', 'created_at', 'purchased_price', 'is_paid']

    fieldsets = [
        ('Main', {
            'fields': [
                'ID', 'expire_at', 'purchased_at', 'purchased_price', 'created_at', 'is_paid', 'stripe_id',
                'stripe_link'
            ],
        }),
        ('Tariff', {
            'fields': ['tariff', 'tariff_price', 'tariff_days'],
        }),
        ('Discounts', {
            'fields': [
                'tariff_discount_name', 'tariff_discount_amount', 'tariff_discount_value', 'tariff_discount_is_percent',
                'user_code_discount_amount', 'user_code_discount_value', 'user_code_discount_is_percent',
            ],
        }),
        ('Student', {
            'fields': ['student', 'student_email', 'student_name', 'student_bonus_amount'],
        }),
        ('Called Student', {
            'fields': [
                'called_student', 'called_student_email', 'called_student_name', 'called_student_code',
                'called_student_bonus_added'
            ],
        }),
    ]

    def get_queryset(self, request):
        return Order.objects.select_related('tariff', 'student', 'called_student')

    def ID(self, obj):
        return '#' + obj.order_id

    def stripe_link(self, obj):
        if obj.stripe_url:
            return format_html(f'<a href="{obj.stripe_url}">{obj.stripe_url}</a>')
        return '-'

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return obj and not obj.is_paid
