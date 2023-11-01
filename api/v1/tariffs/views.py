from django.core.cache import cache
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.utils.translation import get_language
from rest_framework.permissions import IsAuthenticated

from .models import Tariff
from .serializers import TariffSerializer
from api.v1.discounts.models import StudentDiscount, TariffDiscount, TariffDiscountDetail
from api.v1.payments.services import delete_expire_orders
from api.v1.accounts.permissions import IsStudent


class TariffAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsStudent]
    serializer_class = TariffSerializer
    queryset = Tariff.objects.all()

    def get(self, request, *args, **kwargs):
        delete_expire_orders()
        page = str(request.build_absolute_uri())
        page_cache = cache.get(page)
        if page_cache:
            return Response(page_cache)
        serializer = self.get_serializer(self.get_queryset(), many=True)
        tariff_discount_value = 0
        tariff_discount_is_percent = False
        tariff_discount_title = ''
        student_discount_value = 0
        student_discount_is_percent = False
        student_discount = StudentDiscount.objects.first()
        tariff_discount = TariffDiscount.objects.first()

        if student_discount:
            student_discount_value = student_discount.discount_value
            student_discount_is_percent = student_discount.is_percent

        if tariff_discount:
            tariff_discount_value = tariff_discount.discount_value
            tariff_discount_is_percent = tariff_discount.is_percent

            tariff_discount_detail = TariffDiscountDetail.objects.filter(tariff_discount_id=tariff_discount.pk,
                                                                         language_id=get_language()).first()
            if tariff_discount_detail:
                tariff_discount_title = tariff_discount_detail.title

        data = {
            'student_discount_value': student_discount_value,
            'student_discount_is_percent': student_discount_is_percent,
            'tariff_discount_value': tariff_discount_value,
            'tariff_discount_is_percent': tariff_discount_is_percent,
            'tariff_discount_title': tariff_discount_title,
            # 'tariff_discount_image': request.build_absolute_uri(tariff_discount_image),
            'tariff_discount_image': 'https://www.simplilearn.com/ice9/free_resources_article_thumb/what_is_image_Processing.jpg',
            'objects': serializer.data
        }
        cache.set(page, data)
        return Response(data)
