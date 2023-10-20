from django.contrib import admin
from django.utils.html import format_html

from api.v1.general.admin import AbstractTabularInline, AbstractStackedInline
from api.v1.discounts.models import StudentDiscount, TariffDiscount, TariffDiscountDetail


@admin.register(StudentDiscount)
class StudentDiscountAdmin(admin.ModelAdmin):
    list_display = ['discount_value', 'is_percent']

    def has_add_permission(self, request):
        return not StudentDiscount.objects.exists()


class TariffDiscountDetailInline(AbstractStackedInline):
    model = TariffDiscountDetail


@admin.register(TariffDiscount)
class TariffDiscountAdmin(admin.ModelAdmin):
    list_display = ['name', 'img', 'discount_value', 'is_percent']
    list_display_links = ['name', 'discount_value']
    inlines = (TariffDiscountDetailInline,)

    def has_add_permission(self, request):
        return not TariffDiscount.objects.exists()

    def img(self, obj):
        if obj.image:
            return format_html(f"<a href='{obj.image.url}'><img width=80 height=45 src='{obj.image.url}'></a>")
