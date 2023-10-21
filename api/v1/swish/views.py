from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from api.v1.swish.models import MinBonusMoney
from api.v1.swish.permissions import GtMinBonusMoney
from api.v1.swish.serializers import SwishCardSerializer
from api.v1.accounts.permissions import IsStudent


class MinBonusMoneyAPIView(APIView):
    permission_classes = (IsAuthenticated, IsStudent)

    def get(self, request, *args, **kwargs):
        return Response({'min_bonus_money': MinBonusMoney.get_min_bonus_money()})


class SwishCardAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated, IsStudent, GtMinBonusMoney)
    serializer_class = SwishCardSerializer
