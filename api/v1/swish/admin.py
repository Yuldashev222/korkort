from django.contrib import admin

from api.v1.swish.models import SwishCard


@admin.register(SwishCard)
class SwishCardAdmin(admin.ModelAdmin):
    list_display = ['number', 'student', 'student_money', 'created_at', 'is_paid', 'paid_at']
    readonly_fields = ['number', 'student']
    fields = ('student', 'number', 'is_paid', 'paid_at')

    def student_money(self, obj):
        return obj.student.bonus_money
