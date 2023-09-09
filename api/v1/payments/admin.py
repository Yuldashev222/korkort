from django.contrib import admin
from django.utils.html import format_html

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_filter = ['student', 'tariff', 'called_student']
    search_fields = ['student_email', 'tariff_title', 'tariff_discount_title', 'called_student_email']
    list_display = [
        'ID',
        'student',
        'tariff',
        'student_bonus_amount',
        'student_discount_amount',
        'tariff_discount_amount',
        'created_at',
        'tariff_price',
        'purchased_price',
        'is_paid',
    ]
    fieldsets = [
        ('Main', {
            'fields': [
                'ID',
                'expire_at',
                'purchased_at',
                'purchased_price',
                'created_at',
                'is_paid',
                'stripe_id',
                'pay_link',
                'stripe_link'
            ],
        }),
        ('Student', {
            'fields': [
                'student',
                'student_email',
                'student_bonus_amount',
            ],
        }),
        ('Discounts', {
            'fields': [
                'student_discount_amount',
                'student_discount_value',
                'student_discount_is_percent',
                'tariff_discount_title',
                'tariff_discount_amount',
                'tariff_discount_value',
                'tariff_discount_is_percent'

            ],
        }),
        ('Tariff', {
            'fields': [
                'tariff',
                'tariff_title',
                'tariff_price',
                'tariff_days'
            ],
        }),
        ('Called Student', {
            'fields': [
                'called_student',
                'called_student_code',
                'called_student_email',
                'called_student_bonus_added'
            ],
        }),
    ]

    def get_queryset(self, request):
        return Order.objects.select_related('tariff', 'student', 'called_student')

    def ID(self, obj):
        return '#' + obj.order_id

    def pay_link(self, obj):
        if obj.payment_link:
            return format_html(f'<a href="{obj.payment_link}">{obj.payment_link}</a>')
        return '-'

    def stripe_link(self, obj):
        if obj.stripe_url:
            return format_html(f'<a href="{obj.stripe_url}">{obj.stripe_url}</a>')
        return '-'

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
