from django.contrib import admin

from .models import Tariff, TariffDay


class TariffDayAdmin(admin.TabularInline):
    model = TariffDay


@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    inlines = [TariffDayAdmin]

    def has_add_permission(self, request):
        return not Tariff.objects.exists()

    # def delete_model(self, request, obj):
    #     if Order.active_orders().filter(tariff_id=obj.id).exists():
    #         return self.message_user(request,
    #                                  'There are students who have purchased this tariff and are currently using it!')
    #     obj.delete()
