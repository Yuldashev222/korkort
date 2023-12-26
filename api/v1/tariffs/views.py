import os.path

from django.core.cache import cache
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.utils.translation import get_language

from .models import Tariff
from .serializers import TariffSerializer
from api.v1.discounts.models import UserCodeDiscount, TariffDiscount, TariffDiscountDetail


def caching_page(func):
    def wrapping(view, request, *args, **kwargs):
        page = str(request.build_absolute_uri())  # last
        page_cache = cache.get(page)
        if page_cache:
            return Response(page_cache)
        return func(view, request, *args, **kwargs)

    return wrapping


class TariffAPIView(GenericAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = TariffSerializer
    queryset = Tariff.objects.order_by('days')

    @caching_page
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)

        tariff_discount = {
            'title': '',
            'image': None,
            'value': 0,
            'is_percent': False,
        }
        student_discount = {
            'value': 0,
            'is_percent': False,
        }

        student_discount_obj = UserCodeDiscount.objects.first()
        tariff_discount_obj = TariffDiscount.objects.first()

        if student_discount_obj:
            student_discount['value'] = student_discount_obj.discount_value
            student_discount['is_percent'] = student_discount_obj.is_percent

        if tariff_discount_obj:
            tariff_discount['value'] = tariff_discount_obj.discount_value
            tariff_discount['is_percent'] = tariff_discount_obj.is_percent
            tariff_discount['image'] = ('https://www.simplilearn.com/ice9/free_resources_article_thumb/'
                                        'what_is_image_Processing.jpg')

            tariff_discount_detail = TariffDiscountDetail.objects.filter(tariff_discount_id=tariff_discount_obj.pk,
                                                                         language_id=get_language()).first()
            if tariff_discount_detail:
                tariff_discount['title'] = tariff_discount_detail.title

        data = {
            'tariff_discount': tariff_discount,
            'student_discount': student_discount,
            'objects': serializer.data
        }
        return Response(data)
