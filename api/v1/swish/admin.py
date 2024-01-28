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
    list_display = ['number', 'student_name', 'student_money', 'created_at', 'paid_at', 'is_paid']
    fields = ['number', 'student', 'student_email', 'student_name', 'student_money', 'is_paid', 'paid_at', 'created_at']

    def has_add_permission(self, request):
        return False

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = self.fields
        if obj and not obj.is_paid:
            try:
                readonly_fields.remove('is_paid')
            except ValueError:
                pass
        return readonly_fields
