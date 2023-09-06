from django.core.cache import cache
from django.utils.timezone import now
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Tariff
from .serializers import TariffSerializer
from api.v1.accounts.permissions import IsStudent
from api.v1.discounts.models import StudentDiscount


class TariffAPIView(GenericViewSet):
    permission_classes = [IsAuthenticated, IsStudent]
    serializer_class = TariffSerializer
    queryset = Tariff.objects.filter(is_active=True)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        student = self.request.user

        student_discount = cache.get('student_discount')
        if not student_discount:
            StudentDiscount.set_redis()
        student_discount_value = 0
        student_discount_is_percent = False
        if student_discount:
            student_discount_value = student_discount.get('discount_value')
            student_discount_is_percent = student_discount.get('is_percent')

        tariff_discount = cache.get('tariff_discount')
        if not tariff_discount:
            StudentDiscount.set_redis()
        tariff_discount_value = 0
        tariff_discount_is_percent = False
        tariff_discount_title = ''
        tariff_discount_image = None
        # if tariff_discount and tariff_discount['valid_to'] > now().date():
        if tariff_discount:
            tariff_discount_value = tariff_discount.get('discount_value')
            tariff_discount_is_percent = tariff_discount.get('is_percent')
            tariff_discount_title = tariff_discount.get('title')
            tariff_discount_image = tariff_discount.get('image_url')

        return Response({
            'student_discount_value': student_discount_value,
            'student_discount_is_percent': student_discount_is_percent,
            'tariff_discount_value': tariff_discount_value,
            'tariff_discount_is_percent': tariff_discount_is_percent,
            'tariff_discount_title': tariff_discount_title,
            'tariff_discount_image': request.build_absolute_uri(tariff_discount_image),
            'student_bonus_money': student.bonus_money,
            'objects': serializer.data
        })
