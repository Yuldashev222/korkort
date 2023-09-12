from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.discounts.models import TariffDiscount
from api.v1.discounts.serializers import TariffDiscountSerializer


class TariffDiscountAPIView(APIView):
    def get(self, request, *args, **kwargs):

        obj = TariffDiscount.get_tariff_discount()
        if not obj:
            return Response({})
        serializer = TariffDiscountSerializer(obj)
        return Response(serializer.data)
