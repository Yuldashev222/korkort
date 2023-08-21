from django.utils.timezone import now
from rest_framework.permissions import BasePermission


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_staff


class StudentTariffExist(BasePermission):
    def has_permission(self, request, view):
        return request.user.tariff_expire_date > now()
