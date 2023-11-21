from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from api.v1.swish.models import MinBonusMoney, CalledStudentAndSwishTransaction
from api.v1.swish.serializers import SwishCardSerializer, CalledStudentAndSwishTransactionSerializer
from api.v1.general.paginations import CustomPageNumberPagination
from api.v1.accounts.permissions import IsStudent


class SwishCardAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = SwishCardSerializer

    def get(self, request, *args, **kwargs):
        return Response({'min_bonus_money': MinBonusMoney.get_min_bonus_money()})


class CalledStudentAndSwishTransactionAPIView(ListAPIView):
    permission_classes = (IsAuthenticated, IsStudent)
    pagination_class = CustomPageNumberPagination
    serializer_class = CalledStudentAndSwishTransactionSerializer

    def get_queryset(self):
        return CalledStudentAndSwishTransaction.objects.filter(student_email=self.request.user.email
                                                               ).order_by('-created_at')
