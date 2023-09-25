from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Tariff
from .serializers import TariffSerializer
from api.v1.accounts.permissions import IsStudent
from api.v1.discounts.models import StudentDiscount, TariffDiscount


class TariffAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsStudent]
    serializer_class = TariffSerializer
    queryset = Tariff.objects.filter(is_active=True)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        student = self.request.user

        tariff_discount_value = 0
        tariff_discount_is_percent = False
        tariff_discount_title = ''
        tariff_discount_image = None
        student_discount_value = 0
        student_discount_is_percent = False

        student_discount = StudentDiscount.get_student_discount()
        tariff_discount = TariffDiscount.get_tariff_discount()

        if student_discount:
            student_discount_value = student_discount['discount_value']
            student_discount_is_percent = student_discount['is_percent']

        if tariff_discount:
            tariff_discount_value = tariff_discount['discount_value']
            tariff_discount_is_percent = tariff_discount['is_percent']
            tariff_discount_title = tariff_discount['title']
            tariff_discount_image = tariff_discount['image_url']

        return Response({
            'student_discount_value': student_discount_value,
            'student_discount_is_percent': student_discount_is_percent,
            'tariff_discount_value': tariff_discount_value,
            'tariff_discount_is_percent': tariff_discount_is_percent,
            'tariff_discount_title': tariff_discount_title,
            # 'tariff_discount_image': request.build_absolute_uri(tariff_discount_image),
            'tariff_discount_image': 'https://www.simplilearn.com/ice9/free_resources_article_thumb/what_is_image_Processing.jpg',
            'student_bonus_money': student.bonus_money,
            'objects': serializer.data
        })
