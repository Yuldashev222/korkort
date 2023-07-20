from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import TariffDay, Tariff
from .serializers import TariffSerializer, TariffInfoSerializer


class TariffAPIView(GenericViewSet):

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        obj = Tariff.objects.first()
        tariff_info = TariffInfoSerializer(obj).data

        return Response({'tariff_info': tariff_info, 'objects': serializer.data})

    permission_classes = ()
    serializer_class = TariffSerializer
    queryset = TariffDay.objects.filter(is_active=True).order_by('-created_at')
