from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Tariff, TariffInfo
from .serializers import TariffSerializer, TariffInfoSerializer
from api.v1.accounts.permissions import IsStudent


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
        return Response({'tariff_info': tariff_info, 'student_bonus_money': student.bonus_money, 'objects': serializer.data})
