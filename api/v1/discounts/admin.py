from django.contrib import admin
from django.utils.html import format_html

from .models import StudentDiscount, TariffDiscount


@admin.register(StudentDiscount)
class StudentDiscountAdmin(admin.ModelAdmin):
    list_display = ['title', 'discount_value', 'is_percent']
    list_display_links = ['title']

    def has_add_permission(self, request):
        return not StudentDiscount.objects.exists()


@admin.register(TariffDiscount)
class TariffDiscountAdmin(admin.ModelAdmin):
    list_display = ['img', 'title', 'discount_value', 'is_percent']
    list_display_links = ['title']

    def has_add_permission(self, request):
        return not TariffDiscount.objects.exists()

    def img(self, obj):
        if obj.image:
            return format_html(f"<a href='{obj.image.url}'><img width=80 height=45 src='{obj.image.url}'></a>")

