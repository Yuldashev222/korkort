from django.utils.timezone import now
from rest_framework.permissions import BasePermission

from api.v1.swish.models import MinBonusMoney


class GtMinBonusMoney(BasePermission):
    def has_permission(self, request, view):
        min_bonus_money = MinBonusMoney.get_min_bonus_money()
        return min_bonus_money and request.user.bonus_money >= min_bonus_money


class StudentTariffExist(BasePermission):
    def has_permission(self, request, view):
        return request.user.tariff_expire_date > now()
