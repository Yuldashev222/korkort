from django.contrib import admin
from django.core.exceptions import ValidationError

from api.v1.payments.models import Order

from .models import Tariff, TariffAdvantage


@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):

    def delete_model(self, request, obj):
        if Order.active_orders().filter(tariff_id=obj.id).exists():
            return self.message_user(request, 'There are students who have purchased this tariff and are currently using it!')
        obj.delete()
