from django.contrib import admin

from api.v1.swish.models import SwishCard, MinBonusMoney


@admin.register(MinBonusMoney)
class MinBonusMoneyAdmin(admin.ModelAdmin):
    list_display = ['money']
    list_display_links = None
    list_editable = ['money']

    def has_add_permission(self, request):
        return not MinBonusMoney.objects.exists()


@admin.register(SwishCard)
class SwishCardAdmin(admin.ModelAdmin):
    list_display = ['number', 'student', 'created_at', 'is_paid', 'paid_at', 'student_money']
    fields = ('student', 'number', 'is_paid', 'paid_at', 'student_money')

    def has_add_permission(self, request):
        return False

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = ['number', 'student', 'student_money']
        if obj and obj.is_paid:
            readonly_fields.append('is_paid')
        return readonly_fields
