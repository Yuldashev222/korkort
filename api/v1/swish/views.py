from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from api.v1.swish.models import MinBonusMoney, CalledStudentAndSwishTransaction
from api.v1.swish.serializers import SwishCardSerializer, CalledStudentAndSwishTransactionSerializer
from api.v1.general.paginations import CustomPageNumberPagination
from api.v1.accounts.permissions import IsStudent


def page_cache(func):
    def wrapper(view, request, *args, **kwargs):
        return func(view, request, *args, **kwargs)

    return wrapper


class SwishCardAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = SwishCardSerializer

    @page_cache
    def get(self, request, *args, **kwargs):
        obj = MinBonusMoney.objects.first()
        return Response({'min_bonus_money': obj.money if obj is not None else None})


class CalledStudentAndSwishTransactionAPIView(ListAPIView):
    permission_classes = (IsAuthenticated, IsStudent)
    pagination_class = CustomPageNumberPagination
    serializer_class = CalledStudentAndSwishTransactionSerializer

    def get_queryset(self):
        return CalledStudentAndSwishTransaction.objects.filter(student_email=self.request.user.email
                                                               ).order_by('-created_at')
