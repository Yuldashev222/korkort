from django.contrib import admin

from api.v1.swish.models import SwishCard


@admin.register(SwishCard)
class SwishCardAdmin(admin.ModelAdmin):
    list_display = [
        'number', 'student', 'student_money', 'created_at', 'is_paid', 'paid_at', 'is_purchased', 'purchased_price'
    ]
    readonly_fields = ['number', 'student', 'is_purchased', 'purchased_price']
    fields = ('student', 'number', 'is_paid', 'paid_at', 'is_purchased', 'purchased_price')

    def student_money(self, obj):
        return obj.student.bonus_money

    def has_add_permission(self, request):
        return False
