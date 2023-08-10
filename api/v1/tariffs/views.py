from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Tariff, TariffInfo
from .serializers import TariffSerializer, TariffInfoSerializer


class TariffAPIView(GenericViewSet):
    permission_classes = ()
    serializer_class = TariffSerializer
    queryset = Tariff.objects.filter(is_active=True).order_by('-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        obj = TariffInfo.objects.first()
        tariff_info = TariffInfoSerializer(obj).data
        student = self.request.
        return Response({'tariff_info': tariff_info, 'student_bonus_money': '', 'objects': serializer.data})
