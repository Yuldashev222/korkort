from django.core.cache import cache
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Tariff, TariffInfo
from .serializers import TariffSerializer, TariffInfoSerializer
from api.v1.accounts.permissions import IsStudent
from api.v1.discounts.models import StudentDiscount


class TariffAPIView(GenericViewSet):
    permission_classes = [IsAuthenticated, IsStudent]
    serializer_class = TariffSerializer
    queryset = Tariff.objects.filter(is_active=True).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        obj = TariffInfo.objects.first()
        tariff_info = TariffInfoSerializer(obj).data
        student = self.request.user
        student_discount = cache.get('student_discount')
        if not student_discount:
            StudentDiscount.set_redis()

        if not student_discount:
            student_discount_value = 0
            student_discount_is_percent = False
        else:
            student_discount_value = student_discount.get('discount_value')
            student_discount_is_percent = student_discount.get('is_percent')

        return Response({
            'student_discount_value': student_discount_value,
            'student_discount_is_percent': student_discount_is_percent,
            'student_bonus_money': student.bonus_money,
            'tariff_info': tariff_info,
            'objects': serializer.data
        })
