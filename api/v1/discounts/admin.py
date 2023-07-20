from django.contrib import admin

from .models import StudentDiscount, TariffDiscount

admin.site.register([TariffDiscount])


@admin.register(StudentDiscount)
class StudentDiscountAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not StudentDiscount.objects.exists()
